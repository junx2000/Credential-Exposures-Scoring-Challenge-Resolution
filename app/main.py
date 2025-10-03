from typing import List
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
from starlette.concurrency import run_in_threadpool
from schemas import UserScoreResponse
from db import SessionLocal, UserScore
from scoring import fetch_alerts, calculate_user_scores
from config import settings
from logger import logger
from log_middleware import LoggingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Precalcular y guardar los scores al iniciar la API"""

    logger.info("Starting up... Precalculando scores")
    alerts = await run_in_threadpool(fetch_alerts, per_page=settings.MAX_PER_PAGE)
    scores = await run_in_threadpool(calculate_user_scores, alerts)

    db = SessionLocal()
    try:
        for email, score in scores.items():
            user = db.query(UserScore).filter(UserScore.email == email).first()
            if user:
                user.score = score
            else:
                db.add(UserScore(email=email, score=score))
        db.commit()
    finally:
        db.close()
    logger.info("Scores precalculados y guardados en DB al iniciar la API")
    yield

    logger.info("Shutting down...")

app = FastAPI(lifespan=lifespan)
app.add_middleware(LoggingMiddleware)


@app.get("/")
def root():
    return {"message": "API de ejemplo corriendo"}

@app.get("/score/{email}")
def get_user_score(email: str):
    """Consultar el score desde la DB"""
    db = SessionLocal()
    try:
        user = db.query(UserScore).filter(UserScore.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return {"email": user.email, "score": user.score}
    finally:
        db.close()

@app.post("/refresh")
def refresh_scores():
    """Endpoint para recalcular y actualizar los scores en DB"""
    alerts = fetch_alerts(per_page=20)
    scores = calculate_user_scores(alerts)
    db = SessionLocal()
    try:
        for email, score in scores.items():
            user = db.query(UserScore).filter(UserScore.email == email).first()
            if user:
                user.score = score
            else:
                db.add(UserScore(email=email, score=score))
        db.commit()
        return {"status": "ok", "updated_users": len(scores)}
    finally:
        db.close()

@app.get("/score", response_model=List[UserScoreResponse])
def get_all_users_scores():
    """
    Devuelve todos los usuarios y sus scores desde la DB
    """
    db = SessionLocal()
    try:
        users = db.query(UserScore).all()
        return [{"email": u.email, "score": u.score} for u in users]
    finally:
        db.close()
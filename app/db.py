from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class UserScore(Base):
    __tablename__ = "user_scores"
    email = Column(String, primary_key=True, index=True)
    score = Column(Integer)

# Crear las tablas
Base.metadata.create_all(bind=engine)

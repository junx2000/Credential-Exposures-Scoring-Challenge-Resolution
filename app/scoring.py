import time
import requests
from collections import defaultdict
from config import settings
from fastapi import HTTPException


def fetch_alerts(per_page=settings.MAX_PER_PAGE):
    if per_page > settings.MAX_PER_PAGE:
        per_page = settings.MAX_PER_PAGE

    page = 1
    headers = {"X-API-Key": settings.API_KEY}
    all_alerts = []

    while True:
        try:
            resp = requests.get(
                settings.API_URL,
                params={"page": page, "per_page": per_page},
                headers=headers,
                timeout=10
            )
        except requests.exceptions.Timeout:
            print("Request timed out. Reintentando en 30 segundos...")
            time.sleep(30)
            continue
        except requests.exceptions.RequestException as e:
            print(f"Error en la request: {e}")
            raise HTTPException(status_code=503, detail=f"API externa no disponible: {e}") from e

        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 30))
            print(f"Rate limit alcanzado. Esperando {retry_after} segundos...")
            time.sleep(retry_after)
            continue

        resp.raise_for_status()
        data = resp.json()

        alerts = data.get("alerts", [])
        if not alerts:
            break

        all_alerts.extend(alerts)

        total_pages = data.get("total_pages", 1)
        if page >= total_pages:
            break
        page += 1

    return all_alerts

def calculate_user_scores(alerts):
    user_scores = defaultdict(int)

    for alert in alerts:
        email = alert.get("email")
        source = alert.get("source_info", {}).get("source", "")
        severity = alert.get("source_info", {}).get("severity", "low")

        if source == "malware":
            user_scores[email] = 10
            continue

        if source == "data breach":
            if severity == "low":
                user_scores[email] += 1
            elif severity == "high":
                user_scores[email] += 3

        if user_scores[email] > 10:
            user_scores[email] = 10

    return user_scores
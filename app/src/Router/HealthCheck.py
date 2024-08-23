from fastapi import APIRouter, Response
import src.Controller as Controller

HealthCheck = APIRouter()


@HealthCheck.get(path="/healthcheck")
def get_health():
    return Controller.HealthCheck.get_status()
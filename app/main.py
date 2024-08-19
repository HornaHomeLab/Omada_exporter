import os
from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
from prometheus_client import generate_latest

import src.Controller as Controller
import src.Model as Model



app = FastAPI()

@app.get("/metrics")
def get_metrics():
    Controller.PrometheusMetrics.update_switch_metrics()
    Controller.PrometheusMetrics.update_router_metrics()
    Controller.PrometheusMetrics.update_access_point_metrics()
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0",
                port=8000)
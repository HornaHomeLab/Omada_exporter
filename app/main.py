import os
from fastapi import FastAPI, Response
from contextlib import asynccontextmanager
from prometheus_client import generate_latest

import src.Controller as Controller
import src.Model as Model



app = FastAPI()

@app.get("/metrics")
def get_metrics():
    Controller.Devices.AccessPoint.get_info()
    Controller.Devices.Switch.get_info()
    Controller.Devices.Router.get_info()
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0",
                port=8000)
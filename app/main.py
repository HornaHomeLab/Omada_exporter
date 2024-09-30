import uvicorn
from fastapi import FastAPI
import src.Router as Router
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import src.Observability.Trace.OpenTelemetry

app = FastAPI()
app.include_router(Router.Prometheus_router)
app.include_router(Router.HealthCheck)

FastAPIInstrumentor().instrument_app(app)

if __name__ == '__main__':
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000
    )

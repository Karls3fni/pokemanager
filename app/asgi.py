from fastapi import FastAPI
from app.api.healthcheck import router as healthcheck_router
from app.api.trainer import router as trainer_router
from fastapi_pagination import add_pagination

app = FastAPI()
add_pagination(app)

app.include_router(healthcheck_router)
app.include_router(trainer_router)

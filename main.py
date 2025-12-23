from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="Mini Search Engine")

app.include_router(router)

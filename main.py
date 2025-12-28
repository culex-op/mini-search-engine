from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routes import router
from fastapi.responses import FileResponse
app = FastAPI(title="Mini Search Engine")

app.include_router(router)

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
async def home():
    return FileResponse("static/index.html")
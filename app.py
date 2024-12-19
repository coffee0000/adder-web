import os
import uvicorn
from logging import getLogger
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from backend.gateway.auth_router import KEYCLOAK_BASE_URL, router as auth_router
from backend.gateway.middleware import HttpMiddleware
from backend.router.biz_router import router as biz_router
from fastapi.responses import FileResponse, HTMLResponse
import backend.utils

logger = getLogger(__name__)
app = FastAPI()
app.add_middleware(HttpMiddleware)
app.include_router(auth_router, prefix="/oauth2")
app.include_router(biz_router, prefix="/biz")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[KEYCLOAK_BASE_URL], 
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["X-Custom-Header", "Authorization"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="static/assets"), name="assets")


@app.get("/favicon.ico")
async def favicon():
   return FileResponse("static/favicon.ico")


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    with open(os.path.join("static", "index.html")) as file:
        return HTMLResponse(content=file.read())

if __name__ == "__main__":
    uvicorn.run(app)

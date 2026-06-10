from enum import Enum

from fastapi import Cookie, FastAPI, Header, Path, Query, Response
from routes import header, parameters, cookies, issues
# from routes.header import header as header_router # Alternative way to import routes
from core.timer import timing_middleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="API Examples", 
    version="1.0.0",
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health", summary="Simple route example")
async def root():
    return {"status": "ok"}


app.include_router(header.router)
app.include_router(parameters.router)
app.include_router(cookies.router)
app.include_router(issues.router)
app.middleware("http")(timing_middleware)

# CORS middleware example
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "https://myfirstfastapi.onrender.com"  # Agrega aquí tu URL de Render
    ],  # Allow all origins (for testing)
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
    allow_credentials=True,  # Allow cookies and credentials
)


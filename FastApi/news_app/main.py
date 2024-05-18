from fastapi import FastAPI
from app import create_app
from fastapi.middleware.cors import CORSMiddleware

app = create_app()


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173" ,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


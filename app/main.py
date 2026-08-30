from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="WAF Security Operations Lab",
    description="A small API for testing WAF behaviour and web security controls.",
    version="1.0"
)


class LoginRequest(BaseModel):
    username: str
    password: str


@app.get("/")
def home():
    return {"message": "WAF Security Operations Lab is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/login")
def login(details: LoginRequest):
    return {
        "message": "Login request received",
        "username": details.username
    }


@app.get("/api/search")
def search(q: str):
    return {
        "query": q,
        "results": []
    }


@app.get("/api/profile/{username}")
def profile(username: str):
    return {
        "username": username,
        "role": "user"
    }
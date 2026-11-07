from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Partaze API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://partaze.onrender.com", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Partaze API is live"}

@app.get("/health")
def health():
    return {"status": "ok"}

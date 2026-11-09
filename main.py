from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os, httpx

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

TMDB_KEY = os.environ.get("TMDB_API_KEY")

@app.get("/api/search")
async def search_shows(q: str):
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(
            "https://api.themoviedb.org/3/search/multi",
            params={"api_key": TMDB_KEY, "query": q, "include_adult": "false"}
        )
        print("TMDB status:", r.status_code, r.text[:800]) # <- check this in Render Logs
        data = r.json()
    
    out = []
    for s in data.get("results", []):
        if s.get("media_type") not in ("tv", "movie"):
            continue
        out.append({
            "name": s.get("name") or s.get("title"),
            "description": s.get("overview"),
            "poster": f"https://image.tmdb.org/t/p/w500{s['poster_path']}" if s.get("poster_path") else None,
            "rating": s.get("vote_average"),
        })
    return out

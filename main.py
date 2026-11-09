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

TMDB_KEY = os.environ.get("TMDB_API_KEY")

@app.get("/api/search")
async def search_shows(q: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            "https://api.themoviedb.org/3/search/tv",
            params={"api_key": TMDB_KEY, "query": q}
        )
        data = r.json()
    return [{
        "name": s["name"],
        "description": s["overview"],
        "poster": f"https://image.tmdb.org/t/p/w500{s['poster_path']}" if s.get("poster_path") else None,
        "rating": s["vote_average"],
    } for s in data.get("results", [])]

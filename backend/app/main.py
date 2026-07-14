from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import auth, assets, tickets, categories

app = FastAPI(title="ITAsset & Incident Management Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(assets.router)
app.include_router(tickets.router)
app.include_router(categories.router)


@app.get("/api/health")
async def health():
    return {"status": "ok"}

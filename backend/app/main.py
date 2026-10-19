from typing import Annotated

import httpx
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Favorite
from app.schemas import FavoriteCreate, FavoriteOut

CAT_API_URL = "https://api.thecatapi.com/v1/images/search"

app = FastAPI(title="Cat API")

# Typ "databázová session": FastAPI ji automaticky vytvoří přes get_db
DbSession = Annotated[Session, Depends(get_db)]


# Kontrola, že aplikace běží
@app.get("/health")
def health():
    return {"status": "ok"}


# Náhodná kočka z The Cat API
@app.get("/api/cats/random")
async def random_cat():
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(CAT_API_URL)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Cat API je nedostupné")

    cat = response.json()[0]
    return {"id": cat["id"], "url": cat["url"]}


# Seznam oblíbených (nejnovější první)
@app.get("/api/favorites", response_model=list[FavoriteOut])
def list_favorites(db: DbSession):
    return db.scalars(select(Favorite).order_by(Favorite.created_at.desc())).all()


# Uložit kočku do oblíbených
@app.post("/api/favorites", response_model=FavoriteOut, status_code=201)
def add_favorite(data: FavoriteCreate, db: DbSession):
    # Stejnou kočku neuložíme dvakrát
    existing = db.scalar(select(Favorite).where(Favorite.cat_id == data.cat_id))
    if existing:
        raise HTTPException(status_code=409, detail="Kočka už je v oblíbených")

    favorite = Favorite(cat_id=data.cat_id, url=data.url)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)  # načti z databáze id a created_at
    return favorite


# Smazat z oblíbených
@app.delete("/api/favorites/{favorite_id}", status_code=204)
def delete_favorite(favorite_id: int, db: DbSession):
    favorite = db.get(Favorite, favorite_id)
    if favorite is None:
        raise HTTPException(status_code=404, detail="Oblíbená kočka nenalezena")

    db.delete(favorite)
    db.commit()

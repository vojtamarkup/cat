from datetime import datetime

from pydantic import BaseModel, ConfigDict


# Co posílá frontend, když chce uložit kočku
class FavoriteCreate(BaseModel):
    cat_id: str
    url: str


# Co API vrací
class FavoriteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # umí převést objekt z databáze

    id: int
    cat_id: str
    url: str
    created_at: datetime

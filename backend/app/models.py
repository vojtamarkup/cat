from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


# Tabulka "favorites" v databázi
class Favorite(Base):
    __tablename__ = "favorites"

    id: Mapped[int] = mapped_column(primary_key=True)  # naše ID (1, 2, 3...)
    cat_id: Mapped[str] = mapped_column(String(50), unique=True)  # ID kočky z Cat API
    url: Mapped[str] = mapped_column(String(500))  # odkaz na obrázek
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())  # kdy byla uložena

1. Databáze (v `C:\CAT`): docker compose up -d db
2. Backend (v `C:\CAT\backend`): uv run uvicorn app.main:app --reload --port 8000
3. Frontend (v `C:\CAT\frontend`): npm run dev

Images v dockeru budou neaktuální, pokud se změní kód v backendu nebo frontend. V takovém případě je potřeba provést
4. aktualizace docker images (v `C:\CAT`): docker compose build
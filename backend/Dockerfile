#
FROM python:3.14-slim
RUN pip install uv

WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Závislosti (bez dev knihoven jako pytest)
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev

# Kód aplikace a migrace
COPY app ./app
COPY migrations ./migrations
COPY alembic.ini .

# Programy z .venv (uvicorn, alembic) půjdou spustit přímo
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# Při startu: nejdřív migrace databáze, pak server
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
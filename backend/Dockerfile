# ==== base =====
FROM python:3.11-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# OS deps (psycopg2-binary ok sans build; weasyprint évité => PDF_BACKEND=reportlab)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential libpq5 gcc \
 && rm -rf /var/lib/apt/lists/*

# ==== builder (caching des wheels) ====
FROM base AS builder
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheels -r requirements.txt

# ==== runtime ====
FROM base AS runtime
# user non-root
RUN useradd -m appuser
COPY --from=builder /wheels /wheels
RUN pip install --no-index --find-links=/wheels /wheels/* && rm -rf /wheels

# Copier le code
COPY . /app

# Entrée + permissions
RUN mkdir -p /app/staticfiles /app/media && chown -R appuser:appuser /app
USER appuser

# Gunicorn par défaut (ASGI via uvicorn workers)
ENV DJANGO_SETTINGS_MODULE=djouman.settings.production \
    USE_WHITENOISE=true \
    PDF_BACKEND=reportlab \
    CELERY_ENABLED=true

# Exposé (Django derrière Nginx)
EXPOSE 8000

# Entrypoint
COPY ./ops/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

# CMD par défaut = gunicorn
CMD ["gunicorn", "djouman.asgi:application", "-k", "uvicorn.workers.UvicornWorker", "-c", "ops/gunicorn.conf.py"]

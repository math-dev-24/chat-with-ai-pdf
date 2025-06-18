# Utiliser une image Python officielle avec UV préinstallé
FROM python:3.11-slim as base

# Installer UV
RUN pip install uv

# Définir les variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Créer un utilisateur non-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Étape de build pour installer les dépendances
FROM base as builder

# Copier les fichiers de configuration
COPY pyproject.toml .uv ./

# Installer les dépendances avec UV
RUN uv sync --frozen --no-dev

# Étape de production
FROM base as production

# Créer le répertoire de travail
WORKDIR /app

# Copier l'environnement virtuel depuis l'étape de build
COPY --from=builder /root/.cache/uv /root/.cache/uv

# Copier le code source
COPY . .

# Créer les répertoires nécessaires
RUN mkdir -p /app/data/chroma_db /app/data/pdfs && \
    chown -R appuser:appuser /app

# Changer vers l'utilisateur non-root
USER appuser

# Exposer le port
EXPOSE 8000

# Variables d'environnement par défaut
ENV HOST=0.0.0.0 \
    PORT=8000 \
    PDF_PATH=/app/data/pdfs \
    CHROMA_DB_PATH=/app/data/chroma_db

# Commande de démarrage
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 
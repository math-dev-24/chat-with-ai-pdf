# Chat with AI PDF - Backend

Backend API pour l'application de chat avec IA sur des documents PDF.

## 🚀 Installation avec UV

Ce projet utilise [UV](https://github.com/astral-sh/uv) pour la gestion des dépendances Python, qui est plus rapide et plus moderne que pip.

### Prérequis

1. Installer UV :
```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. Redémarrer votre terminal

### Installation du projet

```bash

git clone <your-repo-url>
cd chat-with-ai-pdf/backend

# Créer un environnement virtuel et installer les dépendances
uv sync

# Activer l'environnement virtuel
uv shell
```

### Commandes UV utiles

```bash
# Installer les dépendances
uv sync

# Installer les dépendances de développement
uv sync --dev

# Ajouter une nouvelle dépendance
uv add package-name

# Ajouter une dépendance de développement
uv add --dev package-name

# Supprimer une dépendance
uv remove package-name

# Mettre à jour les dépendances
uv sync --upgrade

# Exécuter une commande dans l'environnement virtuel
uv run python main.py

# Lancer le serveur de développement
uv run uvicorn main:app --reload
```

## 🛠️ Développement

### Structure du projet

```
backend/
├── src/
│   ├── api/           # Endpoints FastAPI
│   ├── application/   # Couche application (adapters, services)
│   ├── domain/        # Couche domaine (ports, services)
│   └── tools/         # Utilitaires
├── data/              # Données (base de données, etc.)
├── main.py           # Point d'entrée de l'application
└── pyproject.toml    # Configuration du projet
```

### Outils de développement

Le projet inclut plusieurs outils de développement configurés :

- **Black** : Formateur de code
- **isort** : Tri des imports
- **flake8** : Linter
- **mypy** : Vérification de types
- **pytest** : Tests unitaires

```bash
# Formater le code
uv run black .

# Trier les imports
uv run isort .

# Linter
uv run flake8 .

# Vérification de types
uv run mypy .

# Lancer les tests
uv run pytest
```

### Variables d'environnement

Créer un fichier `.env` à la racine du backend :

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key
LMSTUDIO_API_KEY=your_lmstudio_api_key

# Configuration de l'application
ENVIRONMENT=development
DEBUG=true
HOST=0.0.0.0
PORT=8000

# Base de données
CHROMA_DB_PATH=./data/chroma_db
```

## 🚀 Démarrage rapide

```bash
# Installer les dépendances
uv sync

# Activer l'environnement virtuel
uv shell

# Lancer le serveur
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

L'API sera disponible sur `http://localhost:8000`

## 📚 Documentation API

Une fois le serveur lancé, la documentation interactive est disponible sur :
- Swagger UI : `http://localhost:8000/docs`
- ReDoc : `http://localhost:8000/redoc`

## 🔧 Migration depuis pip/requirements.txt

Si vous migrez depuis un projet utilisant `requirements.txt` :

1. Supprimer `requirements.txt`
2. Utiliser `uv sync` pour installer les dépendances
3. Remplacer `pip install` par `uv add`
4. Remplacer `pip freeze > requirements.txt` par `uv lock`

## 📦 Dépendances principales

- **FastAPI** : Framework web moderne
- **Uvicorn** : Serveur ASGI
- **LangChain** : Framework pour applications IA
- **ChromaDB** : Base de données vectorielle
- **PyMuPDF** : Traitement de PDF
- **Sentence Transformers** : Modèles d'embeddings
- **Pydantic** : Validation de données 
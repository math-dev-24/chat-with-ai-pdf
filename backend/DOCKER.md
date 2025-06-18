# 🐳 Docker - Chat with AI PDF Backend

Guide pour déployer le backend avec Docker.

## 📋 Prérequis

- Docker installé
- Docker Compose installé
- Variables d'environnement configurées

## 🔧 Configuration

### 1. Variables d'environnement

Créer un fichier `.env` à la racine du backend :

```env
# API Keys
OPENAI_API_KEY=your_openai_api_key_here
LMSTUDIO_API_KEY=your_lmstudio_api_key_here

# Configuration de l'application
ENVIRONMENT=production
DEBUG=false
HOST=0.0.0.0
PORT=8000

# Chemins des données
PDF_PATH=./data/pdfs
CHROMA_DB_PATH=./data/chroma_db
```

### 2. Créer les répertoires de données

```bash
mkdir -p data/pdfs data/chroma_db logs
```

## 🚀 Déploiement

### Production

```bash
# Construire et démarrer le service de production
docker-compose up -d

# Voir les logs
docker-compose logs -f backend

# Arrêter le service
docker-compose down
```

### Développement

```bash
# Démarrer le service de développement
docker-compose --profile dev up -d

# Voir les logs
docker-compose logs -f backend-dev

# Arrêter le service
docker-compose --profile dev down
```

## 🔍 Commandes utiles

```bash
# Reconstruire l'image
docker-compose build --no-cache

# Redémarrer le service
docker-compose restart backend

# Accéder au shell du container
docker-compose exec backend bash

# Voir l'utilisation des ressources
docker stats

# Nettoyer les images non utilisées
docker system prune -a
```

## 📁 Structure des volumes

```
backend/
├── data/
│   ├── pdfs/          # PDFs uploadés
│   └── chroma_db/     # Base de données vectorielle
├── logs/              # Logs de l'application
└── .env               # Variables d'environnement
```

## 🌐 Accès à l'API

- **Production** : http://localhost:8000
- **Développement** : http://localhost:8001
- **Documentation API** : http://localhost:8000/docs

## 🔧 Personnalisation

### Modifier le port

Dans `docker-compose.yml`, changer la ligne :
```yaml
ports:
  - "8000:8000"  # Format: "port_host:port_container"
```

### Ajouter des variables d'environnement

Dans `docker-compose.yml`, section `environment` :
```yaml
environment:
  - NOUVELLE_VARIABLE=valeur
```

### Modifier les volumes

Dans `docker-compose.yml`, section `volumes` :
```yaml
volumes:
  - ./nouveau_chemin:/app/chemin_container
```

## 🐛 Dépannage

### Container ne démarre pas

```bash
# Vérifier les logs
docker-compose logs backend

# Vérifier les variables d'environnement
docker-compose exec backend env

# Redémarrer avec rebuild
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Problème de permissions

```bash
# Corriger les permissions des volumes
sudo chown -R $USER:$USER data/ logs/

# Ou dans le container
docker-compose exec backend chown -R appuser:appuser /app/data
```

### Problème de mémoire

Si l'application consomme trop de mémoire, ajuster dans `docker-compose.yml` :
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 2G
        reservations:
          memory: 1G
```

## 🔒 Sécurité

- L'application s'exécute avec un utilisateur non-root
- Les volumes sont montés en lecture seule quand possible
- Les variables sensibles sont dans le fichier `.env`
- Le healthcheck surveille l'état de l'application

## 📊 Monitoring

### Healthcheck

Le container inclut un healthcheck qui vérifie l'endpoint `/stat` :
```bash
# Vérifier l'état du healthcheck
docker-compose ps
```

### Logs

```bash
# Logs en temps réel
docker-compose logs -f backend

# Logs des dernières 100 lignes
docker-compose logs --tail=100 backend

# Logs avec timestamp
docker-compose logs -t backend
``` 
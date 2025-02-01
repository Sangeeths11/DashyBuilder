# Nuxt 3 Minimal Starter

Look at the [Nuxt 3 documentation](https://nuxt.com/docs/getting-started/introduction) to learn more.

## Setup

Make sure to install the dependencies:

```bash
# npm
npm install

# pnpm
pnpm install

# yarn
yarn install

# bun
bun install
```

## Development Server

Start the development server on `http://localhost:3000`:

```bash
# npm
npm run dev

# pnpm
pnpm run dev

# yarn
yarn dev

# bun
bun run dev
```

## Production

Build the application for production:

```bash
# npm
npm run build

# pnpm
pnpm run build

# yarn
yarn build

# bun
bun run build
```

Locally preview production build:

```bash
# npm
npm run preview

# pnpm
pnpm run preview

# yarn
yarn preview

# bun
bun run preview
```

Check out the [deployment documentation](https://nuxt.com/docs/getting-started/deployment) for more information.


# DashyBuilder Deployment Guide

Dieses Dokument beschreibt, wie du Änderungen an deinem DashyBuilder-Projekt vornehmen und diese in einem Docker-Container deployen kannst.

## Voraussetzungen

- Docker muss auf deinem System installiert sein
- Git für Versionskontrolle
- Node.js und Yarn für lokale Entwicklung

## Entwicklungsumgebung

### Installation der Abhängigkeiten

```bash
# Installation der Projekt-Dependencies
yarn install

# Starten des Entwicklungsservers
yarn dev
```

## Docker Deployment

### 1. Docker Image bauen
```bash
# Neues Image erstellen
docker build -t dashybuilder .

# Überprüfen ob das Image erstellt wurde
docker images
```

### 2. Container Management

#### Container Status überprüfen
```bash
# Alle laufenden Container anzeigen
docker ps

# Alle Container (auch gestoppte) anzeigen
docker ps -a
```

#### Alten Container stoppen und entfernen
```bash
# Container stoppen
docker stop dashybuilder

# Container entfernen
docker rm dashybuilder

# Alternative: Stoppen und Entfernen in einem Befehl
docker rm -f dashybuilder
```

#### Neuen Container starten
```bash
# Container im Hintergrund starten
docker run -d -p 3000:3000 --name dashybuilder dashybuilder

# Container im Vordergrund starten (für Debugging)
docker run -p 3000:3000 --name dashybuilder dashybuilder
```

### 3. Monitoring und Debugging

#### Container Logs
```bash
# Live Logs anzeigen
docker logs -f dashybuilder

# Letzte 100 Log-Zeilen anzeigen
docker logs --tail 100 dashybuilder
```

#### Container Shell
```bash
# Interaktive Shell im Container öffnen
docker exec -it dashybuilder /bin/bash
```

### 4. Schnelle Deployment-Befehle

#### Komplettes Redeployment
```bash
# Stoppen, Entfernen, Neu bauen und Starten in einer Befehlskette
docker rm -f dashybuilder && \
docker build -t dashybuilder . && \
docker run -d -p 3000:3000 --name dashybuilder dashybuilder
```

## Nützliche Docker Befehle

### System Cleanup
```bash
# Nicht verwendete Container, Netzwerke und Images entfernen
docker system prune

# Alle nicht verwendeten Images entfernen
docker image prune -a

# Alle gestoppten Container entfernen
docker container prune
```

### Container Ressourcen
```bash
# Container Ressourcennutzung anzeigen
docker stats dashybuilder

# Detaillierte Container-Informationen
docker inspect dashybuilder
```

## Fehlerbehebung

Wenn der Container nicht startet oder Fehler auftreten:

1. Logs überprüfen:
```bash
docker logs dashybuilder
```

2. Container-Status überprüfen:
```bash
docker ps -a
```

3. In den Container einsteigen:
```bash
docker exec -it dashybuilder /bin/bash
```

## Produktions-Deployment

Für Produktionsumgebungen zusätzliche Parameter setzen:

```bash
docker run -d \
  -p 3000:3000 \
  --name dashybuilder \
  --restart unless-stopped \
  -v /path/to/logs:/app/logs \
  dashybuilder
```

## Entwicklungs-Workflow

1. Lokale Änderungen vornehmen
2. Änderungen testen
3. Git commit und push
4. Neues Docker Image bauen
5. Container neu deployen

## Support

Bei Fragen oder Problemen, bitte ein Issue im Repository erstellen.


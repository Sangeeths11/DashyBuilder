# DashyBuilder

A customizable dashboard tool that enables users to design and manage dynamic dashboards with AI. Built with Vue3, Nuxt, and Supabase, it offers intuitive layout options and exports to Plotly Python code.

![grafik](https://github.com/user-attachments/assets/f09152a3-f557-4019-9c93-9322760a1797)


## Docker

The `docker-compose.yml` file describes the Docker environment with the appropriate containers. For this to function properly, the corresponding environment variables need to be set. This involves copying the `.env.example` file and renaming it to `.env`. Subsequently, the relevant values must be entered into the `.env` file.

To start the environment, the following command is entered in the terminal. This only works if the `docker-compose.yml` file is in the same folder.

### Start

```zsh
docker compose up -d
```

### Stop

```zsh
docker compose down
```

## Frontend

The frontend is implemented using Nuxt 3 and Vue 3. To start the frontend without Docker, you must open the readme in the `DashyBuilder.Frontend` folder. It describes how to start the frontend.

## Backend

The backend is implemented with FastAPI. To start the backend without Docker, open the `app.py` file in the `DashyBuilder.Backend` folder. This file can be started with a Python interpreter.

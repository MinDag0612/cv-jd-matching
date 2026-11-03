# CV x JD Matching

A full-stack CV-JD matching platform powered by FastAPI, Sentence Transformers, and local LLM inference. An application that helps compare a candidate's resume (CV) with a job
description (JD). Users can upload PDF or DOCX documents, extract and edit their
information, then view a match score and feedback for each requirement group.

## Demo

> **Demo video:** _Add a link or embed the demo video here._

## Features

- Read CVs and JDs from PDF or DOCX files.
- Extract information such as skills, education, experience, certificates,
  projects, and job responsibilities.
- Review and edit extracted information before comparing.
- Calculate a similarity score and generate feedback for each JD requirement.
- Provide a React web interface and a FastAPI API.

## Technologies and tools

| Tool | Purpose |
| --- | --- |
| Python | Language for the API and document processing services |
| FastAPI, Uvicorn | Build and run the API |
| [uv](https://docs.astral.sh/uv/) | Manage dependency versions through `uv.lock`, synchronize the environment, and run Python commands |
| `.venv` / `uv venv` | Project-specific Python environment for local development |
| Ollama, `qwen2.5:3b` | Extract information and generate feedback with a language model |
| Sentence Transformers, `all-MiniLM-L6-v2` | Generate embeddings to calculate similarity scores between CVs and JDs |
| React, Vite, Bootstrap | Build the web interface |
| Node.js, npm | Install dependencies and run/build the interface |
| Docker, Docker Compose | Package and run services together |
| Nginx | Serve the built interface and proxy API requests |
| pytest | Run backend tests |

## Prerequisites

### Running with Docker (recommended)

- Docker Desktop or Docker Engine with Docker Compose v2.
- The Docker daemon must be running.
- An Internet connection to build images and download AI models the first time.
- Enough disk space and memory for images, Python/ML dependencies, and the
  Ollama model. The Ollama model is stored in a Docker volume and remains there
  after containers stop.

You do not need to install Python, Node.js, uv, or Ollama on the host machine
when running the entire project with Docker.

### Running locally for development

- Python 3.10 or later.
- [uv](https://docs.astral.sh/uv/getting-started/installation/) to install and
  manage Python dependencies.
- Node.js 22 and npm for the interface (Node.js 22 is also used in the Docker
  build).
- Ollama accessible to the API, with the `qwen2.5:3b` model.
- An Internet connection the first time the Sentence Transformers model
  `sentence-transformers/all-MiniLM-L6-v2` is downloaded.

## Run with Docker Compose

From the repository root:

```powershell
docker compose up --build
```

This command builds and starts the services. The first run may take some time
to download Docker images, install dependencies, and download the
`qwen2.5:3b` model.

Once the services are running:

| Component | URL |
| --- | --- |
| Web interface | <http://localhost:8080> |
| Direct API access | <http://localhost:8000> |
| Swagger API documentation | <http://localhost:8000/docs> |
| Ollama on the host machine | <http://localhost:11435> |

Useful Docker Compose commands:

```powershell
# Run in the background
docker compose up --build -d

# Check service status
docker compose ps

# Follow logs from all services
docker compose logs -f

# Follow API logs
docker compose logs -f api

# Stop and remove containers/network, keeping the downloaded model
docker compose down
```

The Ollama model is kept in the `ollama_data` volume. `docker compose down`
does not remove this volume. Do not add the `-v` flag if you want to keep the
downloaded model.

### Environment variables

When running with Compose, the API receives the Ollama values configured
directly in `docker-compose.yml`:

- `OLLAMA_BASE_URL=http://ollama:11434` — the Ollama address inside the Docker
  network.
- `OLLAMA_TIMEOUT=300` — the Ollama request timeout, in seconds.

This is an internal address between containers; do not use `localhost` for the
API to access Ollama in Compose. Port `11435` is published so Ollama can also
be accessed from the host machine.

## Run locally for development

### 1. Set up Ollama

Install and start Ollama, then download the model:

```powershell
ollama pull qwen2.5:3b
```

By default, the project connects to Ollama at `http://localhost:11435`, as
configured in `.env.sample`. If Ollama runs at a different address, create a
`.env` file from the sample and update `OLLAMA_BASE_URL`:

```powershell
Copy-Item .env.sample .env
```

Example configuration:

```dotenv
OLLAMA_BASE_URL=http://localhost:11435
OLLAMA_TIMEOUT=300
```

`GEMINI_API_KEY` is included in the sample file for future configuration; the
current default flow uses Ollama.

### 2. Install dependencies and run the API

From the repository root:

```powershell
uv sync --extra test
uv run uvicorn app.main:app --reload
```

`uv sync` creates/uses the `.venv` virtual environment and installs the
dependency versions locked in `uv.lock`. `uv run` runs the application in that
environment. You do not need to activate `.venv` manually.

The API runs at <http://localhost:8000>. Open <http://localhost:8000/docs> to
view and try the endpoints.

### 3. Install dependencies and run the interface

Open another terminal:

```powershell
Set-Location ui
npm ci
npm run dev
```

Open the Vite URL shown in the terminal (by default
<http://localhost:5173>). In development mode, Vite proxies `/extractor`
requests to the API at `http://localhost:8000`, so start the API before or
alongside the interface.

### Build the interface

```powershell
Set-Location ui
npm ci
npm run build
```

The build files are created in `ui/dist`.

## Main API endpoints

The main processing endpoints use the `/extractor` prefix:

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/extractor/extract-file` | Accept a PDF/DOCX file and extract CV or JD data |
| `POST` | `/extractor/extract` | Extract data from text content |
| `POST` | `/extractor/compare` | Compare extracted CV and JD data |
| `GET` | `/health1` | Check whether the API is running |

View request/response schemas and try the API at <http://localhost:8000/docs>
while the backend is running.

## How Docker works in this project

Docker Compose coordinates four services:

1. **`ollama`** runs Ollama and stores models in the `ollama_data` volume.
2. **`ollama-init`** waits for Ollama to become healthy, then downloads the
   `qwen2.5:3b` model. The API starts only after the model download completes
   successfully.
3. **`api`** is built from the root `Dockerfile`. The image uses Python 3.12
   and `uv` to install dependencies from the lockfile. Compose mounts the `app`
   directory into the container and runs Uvicorn on port 8000.
4. **`ui`** builds the interface in a Node.js 22 image, then copies `ui/dist`
   into a lightweight Nginx image. Nginx serves the SPA on port 80 and proxies
   `/extractor/` requests to the `api` service on the Compose network.

From the host machine, port 8080 points to Nginx, port 8000 points directly to
the API, and port 11435 points to Ollama. Services communicate with each other
by their service names on the Docker network; for example, the API uses
`http://ollama:11434`.

## Directory structure

```text
.
├── app/
│   ├── core/                 # Configuration, dependencies, and exception handling
│   ├── features/
│   │   ├── extraction/       # Information extraction with AI models
│   │   ├── pairing/          # Pair CV and JD information groups
│   │   ├── parsing/          # Read PDF and DOCX content
│   │   ├── processing/       # Coordinate processing and comparison
│   │   ├── recommendation/   # Generate match feedback
│   │   └── scoring/          # Calculate similarity scores
│   ├── models/               # Data schemas and responses
│   ├── routers/              # API endpoint definitions
│   └── tests/                # Backend tests
├── ui/
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/            # Application pages
│   │   └── services/         # Backend API calls
│   ├── Dockerfile            # Build the frontend and package it with Nginx
│   └── nginx.conf            # Serve the SPA and proxy API requests
├── docker-compose.yml        # Define services and volumes
├── Dockerfile                # Backend image
├── pyproject.toml            # Python project and dependency definitions
├── uv.lock                   # Locked Python dependency versions
└── .env.sample               # Environment variable template for local development
```

## Tests

Run the backend tests:

```powershell
uv sync --extra test
uv run pytest
```

The test that calls Ollama directly requires Ollama to be running and the model
to be downloaded:

```powershell
uv run python app/tests/test.py
```

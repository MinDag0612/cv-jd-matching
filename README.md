# Standalone document extraction services

This folder is an independent copy of the project's PDF/DOCX parser and LLM
information extractor. It does not import the parent project's authentication,
database, or storage code, and the original project files are unchanged.

## API

Start the API from this folder:

```powershell
python -m pip install -e ".[test]"
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` for the interactive API documentation.

- `POST /parser/parse`: parse an uploaded PDF or DOCX into text.
- `POST /extractor/extract`: extract resume or job-description information from
  text. JSON body: `{"text": "...", "is_resume": true}`.
- `POST /extractor/extract-file`: parse an uploaded PDF/DOCX and extract
  information in the same request. Multipart fields: `file` and optional
  `is_resume` (defaults to `false`).
- `GET /health`: API health check.

The extraction endpoints use the Ollama model from `app/core/variable.py`.
Configure `OLLAMA_BASE_URL` and `OLLAMA_TIMEOUT` in this folder's `.env` file.
The default URL is `http://localhost:11435`, matching the copied Compose setup.

## Docker Compose

From this folder, run:

```powershell
docker compose up --build
```

This starts the copied PostgreSQL and Ollama infrastructure, pulls
`qwen2.5:3b`, and starts the API at `http://localhost:8000`. The standalone API
does not use PostgreSQL; the database service is retained from the original
Compose setup.

## Tests

Run service and API unit tests without starting Ollama:

```powershell
python -m pytest
```

The copied `app/tests/test.py` is the original live Ollama smoke test. Run it
from this folder after Ollama is available and the model has been pulled:

```powershell
python app/tests/test.py
```

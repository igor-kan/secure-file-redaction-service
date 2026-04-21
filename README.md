# Secure File Redaction Service

Redacts sensitive regions in uploaded images and returns a sanitized output preview.

## Stack

- FastAPI backend
- Pillow image manipulation
- React frontend uploader/preview

## Run Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8030
```

## Run Frontend

```bash
cd web
npm install
npm run dev
```

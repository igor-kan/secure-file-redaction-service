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

<!-- REPO_ANALYSIS_OVERVIEW_START -->
## Repository Analysis Snapshot

Generated: 2026-04-21

- Primary stack: Unknown
- Key paths: `backend`, `docs`, `.github/workflows`, `README.md`
- Files scanned (capped): 19
- Test signal: Test-named files detected
- CI workflows present: Yes
- GitHub slug: igor-kan/secure-file-redaction-service
- GitHub last push: 2026-04-21T21:14:52Z

### Quick Commands

Setup:
- `Review repository README for setup steps`

Run:
- `Review repository README for run/start command`

Quality:
- `Review CI/workflow commands in .github/workflows`

### Companion Docs

- `AGENTS.md`
- `TASKS.md`
- `PLANNING.md`
- `RESEARCH.md`
- `PROJECT_BRIEF.md`

### Web Research References

- Origin remote: `https://github.com/igor-kan/secure-file-redaction-service.git`
- GitHub homepage: Not set
- `N/A`
<!-- REPO_ANALYSIS_OVERVIEW_END -->

# Operations

## Local
Copy `.env.example` to `.env` and generate unique values for `POSTGRES_PASSWORD` and `SECRET_KEY`. Run `docker compose up --build`.

Image OCR requires the Tesseract binary and Portuguese language pack in the worker container. PDF text extraction is supported; scanned PDFs currently need another OCR adapter.

## CI
Configure GitHub Actions repository secrets `CI_POSTGRES_PASSWORD` and `CI_DJANGO_SECRET_KEY`. Run migrations, backend checks and frontend build before merging.

## Production
Use TLS, a proper WSGI/ASGI server, private receipt storage, secrets management, database backups, Redis monitoring, error reporting, and queue-depth alerts. Do not deploy the development Docker Compose unchanged.

## OCR
Extraction is heuristic, not LLM-backed. Users must explicitly confirm extracted values before they become expenses. No AI model classification or scanned-PDF OCR is implemented.

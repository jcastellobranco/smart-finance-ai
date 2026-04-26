# Smart Finance AI

Smart Finance AI is a full stack expense management platform for couples.

It automates receipt processing using OCR and AI-based classification, allowing users
to upload receipts and automatically extract amount, date, merchant, and expense category.

## Key Features

- Couple/shared household expense management
- Receipt upload
- Async receipt processing
- OCR-based text extraction
- AI expense classification
- Monthly dashboard
- Category-based analytics

## Architecture

Frontend → Django API → Queue → Worker → OCR/AI → PostgreSQL → Dashboard

## Development

Run the app in development mode with Docker:

```bash
docker compose up frontend backend worker db redis
```

The frontend container runs `npm run dev` and mounts `./frontend` into the
container, so normal Vue/Nuxt changes hot reload in the browser. You only need
to rebuild the frontend image after dependency or Dockerfile changes:

```bash
docker compose up --build frontend
```

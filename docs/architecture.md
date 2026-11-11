# Smart Finance AI — architecture

## Decision: modular monolith

Nuxt 4 pages -> Pinia stores -> useApi -> Django REST Framework -> application services/selectors -> Django ORM -> PostgreSQL.

Celery + Redis handles background receipt processing. The system remains one deployable backend with distinct business modules.

## Backend boundaries

- `models.py`: persistence and integrity constraints.
- `serializers.py`: request validation and response representation.
- `views.py`: HTTP adapters.
- `selectors.py`: scoped queries and read-side aggregation.
- `services.py` / `application.py`: transactional write workflows.
- `permissions.py`: resource-level access checks.
- `tasks.py`: background job entrypoints.

Receipt processing depends on expenses for creating a financial entry. Avoid circular application-service dependencies.

## Authorization

Only members can see a household's expenses and receipts. Only owners can modify household details. All financial queries must scope data to authenticated membership.

## Roadmap

Phase 3 replaces the fake receipt extractor with an OCR/AI adapter, normalization and explicit user review.

## Verify

Copy `.env.example` to `.env` and configure secrets, then:

```bash
docker compose up -d db redis
docker compose run --rm backend python manage.py migrate
docker compose run --rm backend python manage.py check
docker compose run --rm backend python manage.py test apps.expenses
```

---
name: Backend testing layout
description: Where backend test types live, the shared db_session fixture, and conventions for writing new tests
type: reference
---

Backend test layout (Python/pytest, asyncio_mode=auto):

- `test/unittest/` — pure unit tests. Two patterns:
  - `test/unittest/use_cases/**` — mock repositories with `mocker.Mock()` + `AsyncMock()` per method. No DB.
  - `test/unittest/repositories/**` — exercise real `BlogRepository`/`UserRepository` against an in-memory SQLite via the shared `db_session` fixture.
- `test/integration/**` and `test/e2e/**` — out of scope for the qa-agent unless explicitly asked.

Key shared fixtures:
- `db_session` (function scope) is defined in **`test/conftest.py`** at the backend root, backed by `sqlite+aiosqlite:///:memory:`. The `setup_database` autouse fixture creates/drops all tables per test. Repository unit tests just declare `db_session: AsyncSession` as a parameter — no extra wiring needed.
- `test/unittest/repositories/utils.py` provides `_normalize_datetime()` for cross-DB tz-aware comparisons (SQLite returns naive datetimes).

Conventions to match when extending these files:
- 2-space indentation throughout test files (project-wide).
- Test methods are async + decorated with `@pytest.mark.asyncio`.
- Use Case tests structure repo mocks as: `repo = mocker.Mock(); repo.<method> = AsyncMock()` inside a class-scoped `blog_repository` fixture.
- Repository tests construct `BlogEntity` directly (no factories yet) and call `repo.create_blog(...)` to seed.
- The semantic public-list filter for blogs is `published_at IS NOT NULL` — NOT `status == "published"`. A published-then-edited blog has `status="draft"` but a non-null `published_at` and must still appear in the public list. Any test for `get_all_public_blogs_by_author` should include this regression case.

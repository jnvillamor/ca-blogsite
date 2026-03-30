---
name: Backend Architecture Overview
description: Clean architecture layers, naming conventions, and file organization for the ca-blogsite backend
type: project
---

The backend follows clean architecture with these layers:

- **Domain layer** (`src/domain/`): entities (`BlogEntity`, `UserEntity`), value objects (`Title`, `Content`, `Password`, `Name`), exceptions (`InvalidDataException`, `NotFoundException`, `UnauthorizedException`)
- **Application layer** (`src/application/`): use cases (`src/application/use_cases/blogs/`, `src/application/use_cases/users/`), DTOs (`src/application/dto/`), repository interfaces (`src/application/repositories/`), service interfaces (`src/application/services/`)
- **Infrastructure layer** (`app/`): ORM models (`app/database/models/`), mappers (`app/database/mappers/`), repository implementations (`app/repositories/`), FastAPI routes (`app/api/v1/`), dependencies (`app/api/dependencies/`)

**Why:** Strict separation enables independent testing of each layer. Use cases depend on interfaces, not implementations.

**How to apply:** When adding new features, follow inside-out: domain entity -> DTO -> use case -> ORM model -> mapper -> repository impl -> route. Mappers convert between entity and model using `to_dict()` pattern. The UoW pattern wraps repositories for transactional operations.

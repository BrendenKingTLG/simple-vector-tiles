# -------------------------------------
# Docker Compose service definitions
# -------------------------------------
IMPORT_SERVICES = postgres import-data import-osm import-wikidata generate-sql import-sql api ui
NO_IMPORT_SERVICES = postgres api ui

# -------------------------------------
# Compose: Full stack (with import)
# -------------------------------------
up:
	docker compose up $(IMPORT_SERVICES)

# -------------------------------------
# Compose: Skip import chain
# -------------------------------------
no-import:
	docker compose up $(NO_IMPORT_SERVICES)

# -------------------------------------
# Compose: Just DB
# -------------------------------------
db:
	docker compose up postgres

# -------------------------------------
# Compose: Clean everything
# -------------------------------------
reset:
	docker compose down -v --remove-orphans

# -------------------------------------
# Compose: Stop all services
# -------------------------------------
stop:
	docker compose down --remove-orphans

# -------------------------------------
# Compose: Rebuild all images
# -------------------------------------
rebuild:
	docker compose build --no-cache

# -------------------------------------
# Poetry: Install dependencies (inside container)
# -------------------------------------
install:
	poetry install

# -------------------------------------
# Poetry: Activate shell (inside container)
# -------------------------------------
shell:
	poetry shell

# -------------------------------------
# Poetry: Run API server manually
# -------------------------------------
run:
	poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000

# -------------------------------------
# Poetry: Lint using Ruff
# -------------------------------------
lint:
	poetry run ruff src

# -------------------------------------
# Poetry: Format code using Black
# -------------------------------------
format:
	poetry run black src

# -------------------------------------
# Poetry: Run tests
# -------------------------------------
test:
	poetry run pytest

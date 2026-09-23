include make/compose.mk
.DEFAULT_GOAL := up

.PHONY: core-check core-demo core-baseline api-check preview
core-check:
	docker compose build core-check
	docker compose run --rm core-check
core-demo:
	docker compose run --rm --build core
core-baseline:
	docker compose run --rm --build core python -m city_core baseline
api-check:
	docker compose build api-check
	docker compose run --rm api-check
preview: up

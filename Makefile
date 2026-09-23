.PHONY: up core-check core-demo core-baseline
up:
	docker compose up -d --build core
core-check:
	docker compose build core-check
	docker compose run --rm core-check
core-demo:
	docker compose run --rm --build core
core-baseline:
	docker compose run --rm --build core python -m city_core baseline

include make/compose.mk
.DEFAULT_GOAL := up

.PHONY: preview
preview:
	docker compose -f docker-compose.yml -f docker-compose.preview.yml up -d --build

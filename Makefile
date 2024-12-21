mongo-reset:
	docker compose down --volumes

mongo-setup:
	docker compose up mongo-setup

redeploy:
	docker compose down
	docker compose build
	docker compose up

start:
	poetry run uvicorn src.server:asgi_app --host 0.0.0.0 --port 3000 --reload

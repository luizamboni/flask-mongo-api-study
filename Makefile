start-dev-containers:
	docker compose down mongo1 mongo2 mongo3 mongo-setup
	docker compose up -d mongo1 mongo2 mongo3 mongo-setup

start-app:
	docker compose down app
	docker compose build app
	docker compose up app

start-fastapi:
	poetry run uvicorn src.fastapi_server:app --host 0.0.0.0 --port 3000 --reload
start-dev-containers:
	docker compose down mongo1 mongo2 mongo3 mongo-sandbox pubsub-emulator gcp-pubsub-emulator-ui
	docker compose up -d mongo1 mongo2 mongo3 mongo-sandbox pubsub-emulator gcp-pubsub-emulator-ui \
		&& sleep 3 \
		&& docker compose up -d mongo-setup

mongo-setup:
	docker compose up mongo-setup

rebuild-and-start-app:
	docker compose down app worker
	docker compose build app worker
	docker compose up app worker

start-app:
	docker compose down app worker
	docker compose up app worker

start-fastapi:
	PYTHONPATH=src poetry run uvicorn src.fastapi_server:app --host 0.0.0.0 --port 3000 --reload


curl-health-sandbox:
	curl -s http://localhost:3000/health \
		-H 'X-Sandbox-Request: true' \
		| jq '.'


curl-health-production:
	curl -s http://localhost:3000/health \
		-H 'X-Sandbox-Request: false' \
		| jq '.'

curl-ticket-list-sandbox:
	curl -s http://localhost:3000/ticket/ \
		-H 'X-Sandbox-Request: true' \
		| jq '.'

curl-ticket-list-production:
	curl -s http://localhost:3000/ticket/ \
		-H 'X-Sandbox-Request: false' \
		| jq '.'

curl-ticket-create-sandbox:
	curl -s -X POST http://localhost:3000/ticket \
		-H 'X-Sandbox-Request: true' \
		-H 'Content-Type: application/json' \
		-d '{"id": "sample-id", "reason": "Example reason"}' \
	| jq '.'

curl-ticket-create-production:
	curl -s -X POST http://localhost:3000/ticket \
		-H 'X-Sandbox-Request: false' \
		-H 'Content-Type: application/json' \
		-d '{"id": "sample-id", "reason": "Example reason"}' \
		| jq '.'

curl-ticket-get-sandbox:
	curl -s http://localhost:3000/ticket/sample-id \
		-H 'X-Sandbox-Request: true' \
		| jq '.'

curl-ticket-get-production:
	curl -s http://localhost:3000/ticket/sample-id \
		-H 'X-Sandbox-Request: false' \
		| jq '.'

curl-ticket-event-sandbox:
	curl -s -X POST http://localhost:3000/ticket/sample-id/event \
		-H 'X-Sandbox-Request: true' \
		-H 'Content-Type: application/json' \
		-d '{"event_type": "status_update", "details": "Set to in_progress"}' \
		| jq '.'

curl-ticket-event-production:
	curl -s -X POST http://localhost:3000/ticket/sample-id/event \
		-H 'X-Sandbox-Request: false' \
		-H 'Content-Type: application/json' \
		-d '{"event_type": "status_update", "details": "Set to in_progress"}' \
		| jq '.'

curl-ticket-cancel-sandbox:
	curl -s -X POST http://localhost:3000/ticket/sample-id/cancel \
		-H 'X-Sandbox-Request: true' \
		-H 'Content-Type: application/json' \
		-d '{"reason": "I didnt like"}' \
		| jq '.'

curl-ticket-cancel-production:
	curl -s -X POST http://localhost:3000/ticket/sample-id/cancel \
		-H 'X-Sandbox-Request: false' \
		-H 'Content-Type: application/json' \
		-d '{"reason": "I didnt like"}' \
		| jq '.'

run-batch-regular:
	PYTHONPATH=src poetry run python -m src.task_sample --env=regular

run-batch-sandbox:
	PYTHONPATH=src poetry run python -m src.task_sample --env=sandbox

docker-run-batch-regular:
	docker compose run --rm app make run-batch-regular

docker-run-batch-sandbox:
	docker compose run --rm app make run-batch-sandbox

run-worker:
	PYTHONPATH=src poetry run python -m src.worker

run-worker-docker:
	docker compose run --rm app make run-worker
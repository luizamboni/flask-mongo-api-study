import os
import asyncio
import logging
from concurrent.futures import TimeoutError as FuturesTimeoutError
from src.initializers.configurator import Configurator
from google.cloud import pubsub_v1
import json
from google.api_core.exceptions import AlreadyExists
from google.cloud import pubsub_v1

PUBSUB_EMULATOR_HOST = os.environ.get("PUBSUB_EMULATOR_HOST", "localhost:8085")
PROJECT_ID = os.environ.get("PUBSUB_PROJECT_ID", "test-project")
SUBSCRIPTION_ID = os.environ.get("PUBSUB_SUBSCRIPTION_ID", "ticket-events-sub")
os.environ["PUBSUB_EMULATOR_HOST"] = PUBSUB_EMULATOR_HOST


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

def setup_pubsub():


    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, "ticket-events")
    try:
        publisher.create_topic(request={"name": topic_path})
        print(f"Created topic: {topic_path}")
    except AlreadyExists:
        print(f"Topic already exists: {topic_path}")

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
    try:
        subscriber.create_subscription(
            request={"name": subscription_path, "topic": topic_path}
        )
        print(f"Created subscription: {subscription_path}")
    except AlreadyExists:
        print(f"Subscription already exists: {subscription_path}")

async def worker():
    logging.debug("Preparing preflight")

    setup_pubsub()

    configurator = Configurator()
    config = await configurator.configure()

    async def callback(message: pubsub_v1.subscriber.message.Message) -> None:

        acked_or_nacked = False  # Ensure ack/nack is only called once

        try:
            # Attempt to parse message attributes as JSON, handle missing/malformed cases
            attributes = {}
            if hasattr(message, "attributes") and message.attributes:
                try:
                    for key, value in message.attributes.items():
                        attributes[key] = value
                        print(f"Attribute {key}: {value}")
                    logging.info("Received attributes: %s", attributes)
                except (json.JSONDecodeError, TypeError) as attr_exc:
                    logging.warning("Malformed or non-JSON attributes: %s; error: %s", message.attributes, attr_exc)
            else:
                logging.info("No attributes found in message.")

            # Attempt to decode message data as UTF-8
            try:

                data = json.loads(message.data.decode("utf-8"))
                logging.info("Received message: %s", data)
            except (AttributeError, UnicodeDecodeError) as decode_exc:
                logging.error("Failed to decode message data: %s", decode_exc)
                message.nack()
                acked_or_nacked = True
                return

            # If all processing succeeded, acknowledge the message
            print(data, attributes)
            environmentConfig = config.regular
            if attributes.get("sandbox") == "true":
                environmentConfig = config.sandbox
            
            ticket_with_cancelation = await environmentConfig.ticket_service.add_event(
                id=data["id"],
                name="cancelled",
                data={
                    "reason": data["reason"]
                }
            )

            message.ack()
            acked_or_nacked = True

        except Exception as exc:
            logging.exception("Error processing message: %s", exc)
            if not acked_or_nacked:
                message.nack()



    with pubsub_v1.SubscriberClient() as subscriber:
        subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_ID)
        logging.info(
            f"Listening for messages on {subscription_path} (emulator at {PUBSUB_EMULATOR_HOST})..."
        )
        future = subscriber.subscribe(subscription_path, callback=asyncio.create_task(callback))
        try:
            future.result()
        except FuturesTimeoutError:
            logging.error("Pub/Sub subscription timed out.")
        except KeyboardInterrupt:
            logging.info("Worker stopped by user.")
            future.cancel()
        except Exception as exc:
            logging.exception("Unexpected error in subscriber: %s", exc)

print("initing worker")
asyncio.run(worker())

from google.cloud import pubsub_v1
from pydantic import BaseModel
from google.api_core.exceptions import NotFound
import os
import json
import logging
from concurrent.futures import TimeoutError


class PubSubConfig(BaseModel):
    host: str | None
    project_id: str
    topic_id: str
    attributes: dict[str,str] = {}

class PubSubPublisherService:
    def __init__(self, config: PubSubConfig):
        self.emulator_host = config.host
        self.project_id = config.project_id
        self.topic_id = config.topic_id
        self.attributes = config.attributes
        if self.emulator_host:
            os.environ["PUBSUB_EMULATOR_HOST"] = self.emulator_host
        self.publisher = pubsub_v1.PublisherClient()
        self.topic_path = self.publisher.topic_path(self.project_id, self.topic_id)
        self._ensure_topic_exists()
  

    def _ensure_topic_exists(self):
        try:
            self.publisher.get_topic(request={"topic": self.topic_path})
        except NotFound:
            self.publisher.create_topic(request={"name": self.topic_path})

    def publish_event(self, message: dict) -> str:

        try:
            serialized_message = json.dumps(message).encode("utf-8")
            logging.error("Publishing message in out: %s: %s, %s", self.topic_path, serialized_message, self.attributes)
            future = self.publisher.publish(
                self.topic_path,
                serialized_message,
                **self.attributes,
            )
            message_id = future.result(timeout=5)
            return message_id
        except TimeoutError as te:
            logging.error("Publishing message timed out: %s", te)
            raise
        except Exception as e:
            logging.error("Failed to publish message: %s", e)
            raise
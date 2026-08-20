"""Cloud Pub/Sub topic event publisher helper."""

from typing import Dict, Any

class PubSubService:
    async def publish_event(self, topic: str, payload: Dict[str, Any]) -> str:
        return f"message-id-{payload.get('job_id', 'unknown')}"

pubsub_service = PubSubService()

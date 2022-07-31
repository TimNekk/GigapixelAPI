from app import models
from app.models import QueueState


def get_token(token: str) -> models.Token | None:
    try:
        return models.Token.get(models.Token.token == token)
    except models.Token.DoesNotExist:
        return None


def get_queues(token: models.Token) -> list[models.Queue]:
    queues = list(models.Queue.select().where(models.Queue.token == token))
    return queues


def get_queue(id: int, token: models.Token | None = None) -> models.Queue | None:
    try:
        queue = models.Queue.get(models.Queue.id == id)
        return queue if not token or queue.token == token else None
    except models.Queue.DoesNotExist:
        return None


def create_queue(token: models.Token) -> models.Queue:
    queue = models.Queue.create(token=token)
    return queue


def set_queue_state(queue_id: int, state: QueueState) -> models.Queue:
    queue = get_queue(queue_id)
    if not queue:
        raise ValueError("Queue not found")
    queue.state = state.value
    queue.save()
    return queue


def remove_quota(token: models.Token) -> models.Token:
    token.quota -= 1
    token.save()
    return token

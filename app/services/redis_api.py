from redis import Redis
from rq import Queue, Retry

from app import crud
from app.config import OUTPUT_PATH, OUTPUT_SUFFIX, IMAGE_DELETION_TIMEOUT
from app.models import QueueState
from app.services.file_managing import delete_image
from app.services.gigapixel_api import process_image

redis = Redis()
redis_queue = Queue(connection=redis)


def add_task(image_b64: str, queue_id: str, scale: str | None = None, mode: str | None = None) -> None:
    task = redis_queue.enqueue(process_image, image_b64, queue_id, scale, mode, retry=Retry(max=3))
    redis_queue.enqueue(crud.set_queue_state, queue_id, QueueState.FINISHED, depends_on=task)
    redis_queue.enqueue_in(IMAGE_DELETION_TIMEOUT, delete_image, OUTPUT_PATH / f"{queue_id}{OUTPUT_SUFFIX}.jpg")

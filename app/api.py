import os

import gigapixel
from fastapi import FastAPI, Depends, HTTPException, status
from starlette.responses import FileResponse

from app.config import OUTPUT_SUFFIX, OUTPUT_PATH
from app.services.auth import verify_token
from app import crud
from app import models
from app import schemas
from app.services.file_managing import is_valid_base64_image
from app.services.redis_api import add_task

app = FastAPI()


@app.get("/", tags=["Root"])
def root():
    return {"message": "Gigapixel API"}


@app.get("/queues", tags=["Queue"], response_model=list[schemas.Queue])
def get_queues(token: models.Token = Depends(verify_token)):
    queues = crud.get_queues(token)
    return queues


@app.get("/queues/{id}", tags=["Queue"], response_model=schemas.Queue)
def get_queue(id: int, token: models.Token = Depends(verify_token)):
    queue = crud.get_queue(id, token)
    if not queue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Queue not found")
    return queue


@app.post("/queues", tags=["Queue"], response_model=schemas.Queue)
def create_queue(queue_create: schemas.QueueCreate, token: models.Token = Depends(verify_token)):
    if token.quota <= 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Quota exceeded")

    if not is_valid_base64_image(queue_create.image_base64):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid image")

    if queue_create.scale not in gigapixel.Scale.__members__.keys():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid scale (must be one of: " + ", ".join(gigapixel.Scale.__members__.keys()) + ")")

    if queue_create.mode not in gigapixel.Mode.__members__.keys():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid mode (must be one of: " + ", ".join(gigapixel.Mode.__members__.keys()) + ")")

    queue = crud.create_queue(token)
    crud.remove_quota(token)

    add_task(queue_create.image_base64, queue.id, queue_create.scale, queue_create.mode)

    return queue


@app.get("/images/{queue_id}", tags=["Image"], response_class=FileResponse)
def get_image(queue_id: int, token: models.Token = Depends(verify_token)):
    queue = crud.get_queue(queue_id, token)
    if not queue:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Queue not found")
    elif queue.state != models.QueueState.FINISHED.value:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Queue not finished")

    path = OUTPUT_PATH / f"{queue_id}{OUTPUT_SUFFIX}.jpg"
    if not os.path.isfile(path):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Image not found")

    return path

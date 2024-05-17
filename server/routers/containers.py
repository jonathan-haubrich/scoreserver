from fastapi import APIRouter
from pydantic import BaseModel
from uuid import UUID

from ..utils.container import Container

router = APIRouter()

@router.get("/containers/{exercise_id}")
async def get_container(exercise_id: UUID) -> UUID:
    """
    Retrieves a container ID based on a given exercise ID or `null` if there's no active container
    """

    return {"container_id": exercise_id}

@router.delete("/containers/{container_id}")
async def delete_container(container_id: UUID):
    """
    Stops a given container container
    """

    container = Container(container_id)

    return {"message": "Success"}

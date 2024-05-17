from fastapi import APIRouter, HTTPException
import os
from pydantic import BaseModel
import random
import re
from uuid import UUID

from ..utils.container import Container
from ..utils.compose_manager import ComposeManager

router = APIRouter()

@router.get("/containers/{exercise_id}")
async def get_container(exercise_id: UUID) -> UUID:
    """
    Retrieves a container ID based on a given exercise ID or `null` if there's no active container
    """

    return {"container_id": exercise_id}

@router.post("/containers/{exercise_id}")
async def build_container(exercise_id: UUID):
    compose_dir = os.getenv("DOCKER_COMPOSE_DIR")
    if compose_dir is None:
        raise HTTPException(status_code=503,
            detail="DOCKER_COMPOSE_DIR is not set, can't find docker compose directory")

    cm = ComposeManager(compose_dir)

    username = ''.join(random.sample("0123456789abcdef", k=8))
    password = ''.join(random.sample("0123456789abcdef", k=8))

    rc, stdout, _ = cm.build("exercise1",
        env={"USERNAME":username, "PASSWORD":password})
    if rc != 0:
        raise HTTPException(status_code=503,
            detail="Failed to build exercise1")

    rc, stdout, _ = cm.port("exercise1", "scoreserver-student")

    output = stdout.decode()
    matches = re.search(r"\d+/tcp -> \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:(\d+)", output)
    port = matches.groups()[0]

    return {
        "username": username,
        "password": password,
        "port": port,
        "command": f"ssh -p{port} {username}@172.20.42.234"
    }

@router.delete("/containers/{container_id}")
async def delete_container(container_id: UUID):
    """
    Stops a given container container
    """

    container = Container(container_id)

    return {"message": "Success"}

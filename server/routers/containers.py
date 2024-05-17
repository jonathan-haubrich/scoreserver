from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import random
import re
from uuid import UUID

from ..utils.container import Container
from ..utils.compose_manager import ComposeManager
import httpx

class Owner(BaseModel):
    owner: str

router = APIRouter()

@router.get("/containers/{exercise_id}")
async def get_container(exercise_id: str):
    """
    Retrieves a container ID based on a given exercise ID or `null` if there's no active container
    """

    # httpx request to a pocketbase endpoint that posts exercise id
    # and returns the container id
    # if no container is found, return null
    #print(exercise_id)
    #now_plus_30 = datetime.now() + timedelta(minutes=30)
    #timestamp = now_plus_30.strftime("%Y-%m-%d %H:%M:%S")
    response = httpx.get(f"http://10.1.2.93:8090/api/collections/sessions/records?expand=exercise&filter=(exercise=\"{exercise_id} AND owner=\")")
    print(response.text)
    if response.status_code == 200:
        container_id = response.json().get("container_id")
    else:
        container_id = None

    return {"container_id": container_id}

@router.post("/containers/{exercise_id}")
async def build_container(exercise_id: str, owner: str):
    print(exercise_id, owner)
    compose_dir = os.getenv("DOCKER_COMPOSE_DIR")
    if compose_dir is None:
        raise HTTPException(status_code=503,
            detail="DOCKER_COMPOSE_DIR is not set, can't find docker compose directory")

    cm = ComposeManager(compose_dir)

    username = ''.join(random.sample("0123456789abcdef", k=8))
    password = ''.join(random.sample("0123456789abcdef", k=8))

    rc, stdout, _ = cm.build(exercise_id,
        env={"USERNAME":username, "PASSWORD":password, "STUDENT_ID":owner})
    if rc != 0:
        raise HTTPException(status_code=503,
            detail="Failed to build exercise1")

    rc, stdout, _ = cm.port(exercise_id, f"scoreserver-student-{owner}")

    output = stdout.decode()
    matches = re.search(r"\d+/tcp -> \d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:(\d+)", output)
    port = matches.groups()[0]

    return JSONResponse(content={
        "id": "exercise01",
        "username": username,
        "password": password,
        "port": port,
        "command": f"ssh -p{port} {username}@192.168.153.128"
    })

@router.delete("/containers/{exercise_id}")
async def delete_container(exercise_id: str):
    """
    Stops a given container container
    """

    compose_dir = os.getenv("DOCKER_COMPOSE_DIR")
    if compose_dir is None:
        raise HTTPException(status_code=503,
            detail="DOCKER_COMPOSE_DIR is not set, can't find docker compose directory")

    cm = ComposeManager(compose_dir)

    rc, stdout, _ = cm.stop(exercise_id)

    return {"message": "Success" if rc==0 else "Failed"}

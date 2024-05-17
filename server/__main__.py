from fastapi import FastAPI
import uvicorn

from .routers import exercises, containers

app = FastAPI()

app.include_router(exercises.router)
app.include_router(containers.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
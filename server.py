from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from uuid import UUID

class AnswerId(BaseModel):
    answer: UUID

app = FastAPI()

@app.post("/exercises/{exercise_id}/submit")
async def submit_answer(exercise_id: UUID, answer: AnswerId):
    # Logic to process the submitted answer
    # ...
    print(f"Answer submitted for exercise {exercise_id}: {answer}")
    return {"message": "Answer submitted successfully"}

@app.get("/exercises/{exercise_id}")
async def get_exercise(exercise_id: UUID):
    # Logic to retrieve the exercise details
    # ...
    return {"exercise_id": exercise_id, "exercise_title": "Exercise Title", "exercise_description": "Exercise Description"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
from fastapi import FastAPI, Depends, HTTPException, Query, status, BackgroundTasks
from sqlalchemy.orm import Session

from .dataset_loader import load_questions
from .schemas import QuestionOut, VerifyAnswerIn
from . import crud
from .dependencies import get_db
from .crud import answer_check

app = FastAPI()


@app.post("/load-dataset/", status_code=status.HTTP_202_ACCEPTED)
async def load_dataset(
        url: str = Query(
            "https://raw.githubusercontent.com/russmatney/go-jeopardy/master/JEOPARDY_CSV.csv",
            examples={
                "ex": {"value": "https://raw.githubusercontent.com/russmatney/go-jeopardy/master/JEOPARDY_CSV.csv"}}
        ),
        max_value: int = Query(1200, examples={"ex": {"value": 1200}}),
        background_tasks: BackgroundTasks = BackgroundTasks(),
):
    """
    Load Jeopardy questions dataset into the database.
    This is a long-running task that runs in the background.
    """

    def load_data():
        from .database import engine, Base
        from sqlalchemy import inspect
        
        # Check if tables exist
        inspector = inspect(engine)
        if not inspector.has_table("questions"):
            # Create tables if they don't exist
            Base.metadata.create_all(bind=engine)
            print("Created database tables")
            
        load_questions(
            url=url,
            max_value=max_value
        )

    background_tasks.add_task(load_data)
    return {"message": "Dataset loading started in the background"}


@app.get(
    "/question/",
    response_model=QuestionOut,
    summary="Get one random question by round & value",
)
def random_question(
        round: str | None = None,
        value: int | None = None,
        db: Session = Depends(get_db),
):
    q = crud.get_random_question(db, round, value)
    if not q:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No question found for given criteria.",
        )
    return q


@app.post("/verify-answer/")
def verify_answer(payload: VerifyAnswerIn, db: Session = Depends(get_db)):
    q = crud.get_question_by_id(db, payload.question_id)
    if not q:
        raise HTTPException(404, "Question ID not found")

    is_correct = answer_check(q.answer, payload.user_answer, q.question)

    return is_correct

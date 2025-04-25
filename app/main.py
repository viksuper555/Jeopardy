from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from .schemas import QuestionOut, VerifyAnswerIn
from . import crud
from .dependencies import get_db
from .crud import answer_check

app = FastAPI()


@app.get(
    "/question/",
    response_model=QuestionOut,
    summary="Get one random question by round & value",
)
def random_question(
        round: str = Query("Jeopardy!", examples={"ex": {"value": "Jeopardy!"}}),
        value: int = Query(200, examples={"ex": {"value": 200}}),
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

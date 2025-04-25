from sqlalchemy.orm import Session
from sqlalchemy import func, select
from . import models


def get_random_question(db: Session, round_: str, value: int) -> models.Question | None:
    """Return one random question matching round & value (uses DB-side random)."""
    stmt = (
        select(models.Question)
        .where(models.Question.round == round_, models.Question.value == value)
        .order_by(func.random())
        .limit(1)
    )
    return db.scalar(stmt)


def get_question_by_id(db: Session, qid: int) -> models.Question | None:
    return db.get(models.Question, qid)

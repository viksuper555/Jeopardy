import json

from sqlalchemy.orm import Session
from sqlalchemy import func, select
from . import models
from .chains import verifier_chain


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


_SIMPLIFY = str.maketrans("", "", " .,!?:;\"'()[]{}")


def _normalize(txt: str) -> str:
    return txt.lower().translate(_SIMPLIFY).strip()


def answer_check(correct: str, user: str, question: str | None = None) -> bool:
    """
    Returns (is_correct, explanation_or_none)
    """
    # First do a local check
    if _normalize(correct) == _normalize(user):
        return True

    response = verifier_chain.invoke({
        "question": question or "",
        "correct_answer": correct,
        "user_answer": user
    })
    if hasattr(response, "content"):
        raw = response.content
    elif isinstance(response, (list, tuple)) and hasattr(response[0], "content"):
        raw = response[0].content
    else:
        raw = str(response)
    try:
        result = json.loads(raw)
        return result.get("is_correct", False)
    except json.JSONDecodeError:
        return False

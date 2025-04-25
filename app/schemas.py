from pydantic import BaseModel, Field

class QuestionOut(BaseModel):
    question_id: int = Field(..., alias="id")
    round: str
    category: str
    value: int
    question: str

    class Config:
        orm_mode = True
        validate_by_name = True


class VerifyAnswerIn(BaseModel):
    question_id: int
    user_answer: str


class VerifyAnswerOut(BaseModel):
    is_correct: bool
    ai_response: str | None = None

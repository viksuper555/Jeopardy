from pydantic import BaseModel, Field

class QuestionOut(BaseModel):
    question_id: int = Field(..., alias="id")
    round: str
    category: str
    value: int
    question: str

    class Config:
        from_attributes = True
        validate_by_name = True


class VerifyAnswerIn(BaseModel):
    question_id: int
    user_answer: str

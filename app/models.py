from sqlalchemy import Column, Integer, String, Date
from .database import Base


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    show_number = Column(String, index=True)
    air_date = Column(Date, index=True)
    round = Column(String, index=True)
    category = Column(String, index=True)
    value = Column(Integer, index=True)
    question = Column(String, unique=True, index=True)
    answer = Column(String, index=True)

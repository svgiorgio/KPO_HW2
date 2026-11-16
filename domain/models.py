from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid

class DomainException(Exception):
    pass

class InvalidScoreException(DomainException):
    pass

@dataclass(frozen=True)
class StudentId:
    value: str

@dataclass(frozen=True)
class CriterionId:
    value: str

@dataclass(frozen=True)
class Score:
    value: float

    def __post_init__(self):
        if self.value < 0:
            raise InvalidScoreException("Балл не может быть отрицательным")

@dataclass(frozen=True)
class Weight:
    value: float

    def __post_init__(self):
        if self.value <= 0:
            raise InvalidScoreException("Вес должен быть положительным")

class Student:
    def __init__(self, student_id: StudentId, name: str):
        self.id = student_id
        self.name = name

class Criterion:
    def __init__(self, criterion_id: CriterionId, name: str, max_score: float, weight: Weight):
        self.id = criterion_id
        self.name = name
        self.max_score = max_score
        self.weight = weight

class Evaluation:
    def __init__(self, evaluation_id: str, student_id: StudentId, criterion_id: CriterionId, score: Score):
        self.id = evaluation_id
        self.student_id = student_id
        self.criterion_id = criterion_id
        self.score = score

class EvaluationFactory:
    @staticmethod
    def create(student_id: StudentId, criterion: Criterion, score_value: float) -> Evaluation:
        if score_value > criterion.max_score:
            raise InvalidScoreException(
                f"Балл {score_value} превышает максимум критерия {criterion.name} ({criterion.max_score})"
            )
        score = Score(score_value)
        eval_id = str(uuid.uuid4())
        return Evaluation(eval_id, student_id, criterion.id, score)
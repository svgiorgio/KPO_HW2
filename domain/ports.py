from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Student, Criterion, Evaluation, StudentId, CriterionId

class StudentRepository(ABC):
    @abstractmethod
    def save(self, student: Student) -> None:
        pass

    @abstractmethod
    def get_by_id(self, student_id: StudentId) -> Optional[Student]:
        pass

    @abstractmethod
    def get_all(self) -> List[Student]:
        pass


class CriterionRepository(ABC):
    @abstractmethod
    def save(self, criterion: Criterion) -> None:
        pass

    @abstractmethod
    def get_by_id(self, criterion_id: CriterionId) -> Optional[Criterion]:
        pass

    @abstractmethod
    def get_all(self) -> List[Criterion]:
        pass


class EvaluationRepository(ABC):
    @abstractmethod
    def save(self, evaluation: Evaluation) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[Evaluation]:
        pass

    @abstractmethod
    def get_by_student(self, student_id: StudentId) -> List[Evaluation]:
        pass
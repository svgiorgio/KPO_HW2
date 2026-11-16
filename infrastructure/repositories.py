from typing import List, Optional
from domain.ports import StudentRepository, CriterionRepository, EvaluationRepository
from domain.models import Student, Criterion, Evaluation, StudentId, CriterionId


class InMemoryStudentRepository(StudentRepository):
    def __init__(self):
        self._storage = {}

    def save(self, student: Student) -> None:
        self._storage[student.id.value] = student

    def get_by_id(self, student_id: StudentId) -> Optional[Student]:
        return self._storage.get(student_id.value)

    def get_all(self) -> List[Student]:
        return list(self._storage.values())


class InMemoryCriterionRepository(CriterionRepository):
    def __init__(self):
        self._storage = {}

    def save(self, criterion: Criterion) -> None:
        self._storage[criterion.id.value] = criterion

    def get_by_id(self, criterion_id: CriterionId) -> Optional[Criterion]:
        return self._storage.get(criterion_id.value)

    def get_all(self) -> List[Criterion]:
        return list(self._storage.values())


class InMemoryEvaluationRepository(EvaluationRepository):
    def __init__(self):
        self._storage = {}

    def save(self, evaluation: Evaluation) -> None:
        self._storage[evaluation.id] = evaluation

    def get_all(self) -> List[Evaluation]:
        return list(self._storage.values())

    def get_by_student(self, student_id: StudentId) -> List[Evaluation]:
        return [ev for ev in self._storage.values() if ev.student_id.value == student_id.value]
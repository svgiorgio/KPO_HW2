from domain.ports import StudentRepository, CriterionRepository, EvaluationRepository
from domain.models import Student, StudentId, Criterion, CriterionId, EvaluationFactory, Weight
from domain.services import GradeCalculator
from typing import List, Dict


class AddStudentUseCase:
    def __init__(self, student_repo: StudentRepository):
        self.student_repo = student_repo

    def execute(self, student_id: str, name: str) -> None:
        student = Student(StudentId(student_id), name)
        self.student_repo.save(student)


class AddCriterionUseCase:
    def __init__(self, criterion_repo: CriterionRepository):
        self.criterion_repo = criterion_repo

    def execute(self, criterion_id: str, name: str, max_score: float, weight_value: float) -> None:
        weight = Weight(weight_value)
        criterion = Criterion(CriterionId(criterion_id), name, max_score, weight)
        self.criterion_repo.save(criterion)


class CreateEvaluationUseCase:
    def __init__(self, student_repo: StudentRepository, criterion_repo: CriterionRepository,
                 evaluation_repo: EvaluationRepository):
        self.student_repo = student_repo
        self.criterion_repo = criterion_repo
        self.evaluation_repo = evaluation_repo

    def execute(self, student_id: str, criterion_id: str, score_value: float) -> None:
        student = self.student_repo.get_by_id(StudentId(student_id))
        if not student:
            raise ValueError(f"Студент {student_id} не найден")

        criterion = self.criterion_repo.get_by_id(CriterionId(criterion_id))
        if not criterion:
            raise ValueError(f"Критерий {criterion_id} не найден")

        evaluation = EvaluationFactory.create(student.id, criterion, score_value)
        self.evaluation_repo.save(evaluation)


class CalculateFinalGradesUseCase:
    def __init__(self, criterion_repo: CriterionRepository, evaluation_repo: EvaluationRepository,
                 calculator: GradeCalculator):
        self.criterion_repo = criterion_repo
        self.evaluation_repo = evaluation_repo
        self.calculator = calculator

    def execute(self) -> Dict[str, float]:
        criteria = self.criterion_repo.get_all()
        evaluations = self.evaluation_repo.get_all()

        raw_results = self.calculator.calculate_final_grades(criteria, evaluations)

        return {k.value: v for k, v in raw_results.items()}
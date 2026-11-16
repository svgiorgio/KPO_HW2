from infrastructure.di import Container
from application.use_cases import (
    AddStudentUseCase,
    AddCriterionUseCase,
    CreateEvaluationUseCase,
    CalculateFinalGradesUseCase
)
from domain.models import DomainException, StudentId
from infrastructure.repositories import InMemoryStudentRepository


class ConsoleUI:
    def __init__(self, container: Container):
        self.container = container

        self.add_student = container.resolve(AddStudentUseCase)
        self.add_criterion = container.resolve(AddCriterionUseCase)
        self.create_evaluation = container.resolve(CreateEvaluationUseCase)
        self.calc_grades = container.resolve(CalculateFinalGradesUseCase)
        self.student_repo = container.resolve(InMemoryStudentRepository)

    def run_demo(self):
        print("--- Система ПОС ---\n")

        print("1. Добавление данных")
        self.add_student.execute("s1", "Георгий Светличный")
        print("  + Добавлен студент: Георгий Светличный")

        self.add_student.execute("s2", "Иван Иванов")
        print("  + Добавлен студент: Иван Иванов")

        self.add_criterion.execute("c1", "Домашнее задание", max_score=10.0, weight_value=0.4)
        print("  + Добавлен критерий: Домашнее задание (вес: 0.4)")

        self.add_criterion.execute("c2", "Экзамен", max_score=10.0, weight_value=0.6)
        print("  + Добавлен критерий: Экзамен (вес: 0.6)")

        print("\n2. Выставление оценок")
        self.create_evaluation.execute("s1", "c1", 9.0)
        self.create_evaluation.execute("s1", "c2", 8.0)
        print("  * Студент Георгий Светличный получил оценки: 9.0 (ДЗ), 8.0 (Экзамен)")

        self.create_evaluation.execute("s2", "c1", 7.0)
        self.create_evaluation.execute("s2", "c2", 6.0)
        print("  * Студент Иван Иванов получил оценки: 7.0 (ДЗ), 6.0 (Экзамен)")

        print("\n3. Проверка защиты домена (инварианты)")
        try:
            self.create_evaluation.execute("s1", "c1", 12.0)
        except DomainException as e:
            print(f"  ! Попытка поставить 12/10: отклонено. Причина: {e}")

        try:
            self.create_evaluation.execute("s1", "c3", 5.0)
        except ValueError:
            print("  ! Попытка оценить по несуществующему критерию c3: отклонено.")

        print("\n4. Итоговые результаты")
        results = self.calc_grades.execute()

        for student_id, final_grade in results.items():
            student = self.student_repo.get_by_id(StudentId(student_id))
            name = student.name if student else student_id
            print(f"  {name}: итоговый балл = {round(final_grade, 2)}")

        print("\n--- Работа модуля завершена ---")
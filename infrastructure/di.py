from infrastructure.repositories import (
    InMemoryStudentRepository,
    InMemoryCriterionRepository,
    InMemoryEvaluationRepository
)
from domain.services import GradeCalculator, WeightedSumStrategy
from application.use_cases import (
    AddStudentUseCase,
    AddCriterionUseCase,
    CreateEvaluationUseCase,
    CalculateFinalGradesUseCase
)


class Container:
    def __init__(self):
        self._factories = {}
        self._singletons = {}

        self._register_dependencies()

    def _register_dependencies(self):
        self._singletons[InMemoryStudentRepository] = InMemoryStudentRepository()
        self._singletons[InMemoryCriterionRepository] = InMemoryCriterionRepository()
        self._singletons[InMemoryEvaluationRepository] = InMemoryEvaluationRepository()

        self._singletons[GradeCalculator] = GradeCalculator(WeightedSumStrategy())

        self._factories[AddStudentUseCase] = lambda: AddStudentUseCase(
            self.resolve(InMemoryStudentRepository)
        )
        self._factories[AddCriterionUseCase] = lambda: AddCriterionUseCase(
            self.resolve(InMemoryCriterionRepository)
        )
        self._factories[CreateEvaluationUseCase] = lambda: CreateEvaluationUseCase(
            self.resolve(InMemoryStudentRepository),
            self.resolve(InMemoryCriterionRepository),
            self.resolve(InMemoryEvaluationRepository)
        )
        self._factories[CalculateFinalGradesUseCase] = lambda: CalculateFinalGradesUseCase(
            self.resolve(InMemoryCriterionRepository),
            self.resolve(InMemoryEvaluationRepository),
            self.resolve(GradeCalculator)
        )

    def resolve(self, key):
        if key in self._singletons:
            return self._singletons[key]
        if key in self._factories:
            return self._factories[key]()
        raise ValueError(f"Зависимость {key} не зарегистрирована")
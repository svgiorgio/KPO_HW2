from abc import ABC, abstractmethod
from typing import List, Dict
from .models import StudentId, Criterion, Evaluation


class GradeStrategy(ABC):
    @abstractmethod
    def calculate(self, criteria: List[Criterion], evaluations: List[Evaluation]) -> Dict[StudentId, float]:
        pass


class WeightedSumStrategy(GradeStrategy):
    def calculate(self, criteria: List[Criterion], evaluations: List[Evaluation]) -> Dict[StudentId, float]:
        max_scores = {c.id.value: c.max_score for c in criteria}
        weights = {c.id.value: c.weight.value for c in criteria}

        results = {}
        for ev in evaluations:
            if ev.student_id not in results:
                results[ev.student_id] = 0.0

            crit_id = ev.criterion_id.value
            if crit_id in weights and crit_id in max_scores:
                max_s = max_scores[crit_id]
                if max_s > 0:
                    normalized_score = (ev.score.value / max_s) * 10.0
                    results[ev.student_id] += normalized_score * weights[crit_id]

        return results


class GradeCalculator:
    def __init__(self, strategy: GradeStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: GradeStrategy):
        self._strategy = strategy

    def calculate_final_grades(self, criteria: List[Criterion], evaluations: List[Evaluation]) -> Dict[
        StudentId, float]:
        return self._strategy.calculate(criteria, evaluations)
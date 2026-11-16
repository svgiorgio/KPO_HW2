import unittest
from domain.models import (
    EvaluationFactory,
    Criterion,
    CriterionId,
    StudentId,
    Weight,
    InvalidScoreException
)
from domain.services import GradeCalculator, WeightedSumStrategy


class TestDomain(unittest.TestCase):

    def test_evaluation_factory_score_invariant(self):
        crit = Criterion(CriterionId("c1"), "Тест", max_score=10.0, weight=Weight(1.0))

        ev = EvaluationFactory.create(StudentId("s1"), crit, 8.5)
        self.assertEqual(ev.score.value, 8.5)

        with self.assertRaises(InvalidScoreException):
            EvaluationFactory.create(StudentId("s1"), crit, 11.0)

    def test_negative_score_invariant(self):
        with self.assertRaises(InvalidScoreException):
            EvaluationFactory.create(
                StudentId("s1"),
                Criterion(CriterionId("c1"), "Тест", max_score=10.0, weight=Weight(1.0)),
                -1.0
            )

    def test_criterion_weight_invariant(self):
        with self.assertRaises(InvalidScoreException):
            Criterion(CriterionId("c1"), "Тест", max_score=10.0, weight=Weight(-0.5))

    def test_grade_calculator_weighted_sum(self):
        crit1 = Criterion(CriterionId("c1"), "ДЗ", max_score=10.0, weight=Weight(0.4))
        crit2 = Criterion(CriterionId("c2"), "Экзамен", max_score=20.0, weight=Weight(0.6))

        ev1 = EvaluationFactory.create(StudentId("s1"), crit1, 8.0)
        ev2 = EvaluationFactory.create(StudentId("s1"), crit2, 10.0)

        calc = GradeCalculator(WeightedSumStrategy())
        results = calc.calculate_final_grades([crit1, crit2], [ev1, ev2])

        self.assertAlmostEqual(results[StudentId("s1")], 6.2)

    def test_grade_calculator_empty_student(self):
        crit = Criterion(CriterionId("c1"), "Тест", max_score=10.0, weight=Weight(1.0))
        calc = GradeCalculator(WeightedSumStrategy())

        results = calc.calculate_final_grades([crit], [])
        self.assertEqual(len(results), 0)


if __name__ == '__main__':
    unittest.main()
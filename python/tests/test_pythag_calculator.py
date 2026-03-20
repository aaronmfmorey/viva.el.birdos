import unittest
from utils import pythag_calculator


class TestPythagCalculator(unittest.TestCase):

    def test_default_case(self):
        """
        Test that the default options work correctly.
        """
        self.assertEqual(
            round(pythag_calculator.calculate_pythag_wins(200, 150), 2), 101.84
        )

    def test_setting_number_of_games(self):
        """
        Test that the default options work correctly.
        """
        self.assertEqual(
            pythag_calculator.calculate_pythag_wins(200, 200, games=81),
            40.5,
        )

    def test_setting_exponent(self):
        """
        Test that the default options work correctly.
        """
        self.assertEqual(
            round(pythag_calculator.calculate_pythag_wins(200, 150, exponent=2), 2),
            103.68,
        )

    def test_2025_padres(self):
        """
        Test that the default options work correctly.
        """
        self.assertEqual(round(pythag_calculator.calculate_pythag_wins(702, 621)), 90)

    def test_2025_rockies(self):
        """
        Test that the default options work correctly.
        """
        self.assertEqual(round(pythag_calculator.calculate_pythag_wins(597, 1021)), 44)


if __name__ == "__main__":
    unittest.main()

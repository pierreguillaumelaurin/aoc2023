from src.coordinates import Coordinates, translate


class TestTranslate:
    def test_when_positive_translation(self):
        assert translate((4, 6), (1, 1)) == Coordinates(5, 7)

    def test_when_negative_translation(self):
        assert translate((4, 6), (-1, -1)) == Coordinates(3, 5)

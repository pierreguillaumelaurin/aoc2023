from src.day01.day01 import to_calibration, to_digit_numbers_only


class TestToCalibration:
    class TestGivenOneDigitInString:
        def test_it_should_return_first_and_last_number(self):
            assert to_calibration("treb7uchet") == 77

    class TestGivenTwoDigitInString:
        def test_it_should_return_first_and_last_number(self):
            assert to_calibration("pqr3stu8vwx") == 38

        class TestWhenOneOfTheNumberIsZero:
            def test_it_should_return_one_number_only(self):
                assert to_calibration("aos0cb8") == 8


class TestToDigitNumbersOnly:
    def test_when_string_digits_at_start_and_end(self):
        assert to_digit_numbers_only("two1nine") == "219"

    def test_when_three_string_digits(self):
        assert to_digit_numbers_only("eightwothree") == "8wo3"

    def test_when_digits_and_letters(self):
        assert to_digit_numbers_only("abcone2threexyz") == "abc123xyz"

    def test_when_digits_overlapping(self):
        assert to_digit_numbers_only("xtwone3four") == "x2ne34"
        assert to_digit_numbers_only("zoneight234") == "z1ight234"

    def test_when_border_numbers_are_digits(self):
        assert to_digit_numbers_only("4nineeightseven2") == "49872"
        assert to_digit_numbers_only("7pqrstsixteen") == "7pqrst6teen"

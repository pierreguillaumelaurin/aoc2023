from src.day01.day01 import part_two, to_calibration


class TestPartOne:
    class TestGivenOneDigitInString:
        def test_it_should_return_first_and_last_number(self):
            assert to_calibration("treb7uchet") == 77

    class TestGivenTwoDigitInString:
        def test_it_should_return_first_and_last_number(self):
            assert to_calibration("pqr3stu8vwx") == 38

        class TestWhenOneOfTheNumberIsZero:
            def test_it_should_return_one_number_only(self):
                assert to_calibration("aos0cb8") == 8


class TestPartTwo:
    def test_when_string_digits_at_start_and_end(self):
        assert part_two(["two1nine"]) == 29

    def test_when_three_string_digits(self):
        assert part_two(["eightwothree"]) == 83
        assert part_two(["sevenfourfour99seven8"]) == 78
        assert part_two(["fivenhcvbntlcfthreemsktzr9two"]) == 52

    def test_when_digits_and_letters(self):
        assert part_two(["abcone2threexyz"]) == 13

    def test_when_digits_overlapping(self):
        assert part_two(["xtwone3four"]) == 24
        assert part_two(["zoneight234"]) == 14

    def test_when_border_numbers_are_digits(self):
        assert part_two(["4nineeightseven2"]) == 42
        assert part_two(["7pqrstsixteen"]) == 76

    def test_when_longest_input(self):
        assert (
            part_two(["psgqgrbhsdvhgdxvbdqcxmstnhnqmhchjmbtsdll5qrhlngzzonetwoneg"])
            == 51
        )

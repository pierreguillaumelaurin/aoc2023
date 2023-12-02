class TestToCalibration:
    class TestGivenOneDigitInString:
        def test_it_should_return_first_and_last_number(self):
            assert to_calibration("treb7uchet") == 77

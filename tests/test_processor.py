import unittest
from unittest.mock import patch
from io import StringIO
from processor import process_weather_data

class TestProcessor(unittest.TestCase):

    def test_process_weather_data_empty_message(self):
        # test with an empty message body

        empty_message = {
            'Body': ''
        }

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            process_weather_data(empty_message)
            output = mock_stdout.getvalue().strip()
            self.assertIn("Empty message received", output)

    def test_process_weather_data_wrong_json_format(self):
        # test with wrong data format
        wrong_json_message = {
            'Body': 'test test'
        }

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            process_weather_data(wrong_json_message)
            output = mock_stdout.getvalue().strip()
            self.assertIn("Failed to decode JSON", output)
            self.assertIn("raw message was: test test", output)

if __name__ == '__main__':
    unittest.main()

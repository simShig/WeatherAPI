import unittest
from unittest.mock import patch, MagicMock
from scheduler import get_weather_data
from io import StringIO
class TestScheduler(unittest.TestCase):

    def test_get_weather_data_real_city(self):
        # Test with a valid city, expecting a successful response
        result = get_weather_data('London')
        print (result)
        self.assertIsNotNone(result)
        self.assertIn("location", result)
        self.assertEqual(result["location"]["name"], "London")

    def test_get_weather_data_non_existing_city(self):
        # Test with a non-existing city, expecting a None response
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = get_weather_data('blablabla')
            output = mock_stdout.getvalue().strip()
            self.assertIsNone(result)
            self.assertIn("(city unavailable)", output)
            print(result)

    @patch('scheduler.requests.get')
    def test_get_weather_data_connection_failure(self, mock_get):
        # Mock a connection failure (status code 500)
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = get_weather_data('London')
            output = mock_stdout.getvalue().strip()
            self.assertIsNone(result)
            self.assertIn("connection issue", output)
            print(result)

if __name__ == '__main__':
    unittest.main()

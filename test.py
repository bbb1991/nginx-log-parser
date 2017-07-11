import datetime
import unittest
import settings
from datetime import datetime as dt

str_date = "02/Jul/2017:03:18:10 +0000"


class TestDateTimeConversion(unittest.TestCase):
    def test_conversion(self):
        log_time = dt.strptime(str_date, settings.DATETIME_FORMAT)
        expect_time = datetime.datetime(2017, 7, 2, 3, 18, 10, tzinfo=datetime.timezone.utc)
        # print(log_time)

        self.assertEqual(expect_time, log_time, log_time)


if __name__ == '__main__':
    unittest.main()

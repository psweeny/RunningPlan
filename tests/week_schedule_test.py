from unittest import TestCase
from week_schedule import WeekSchedule, SessionType
import datetime as dt

MONDAY_DATE = dt.date(2025, 6, 16)


class WeekScheduleTest(TestCase):

    def test_week_name_is_W_and_week_number(self):
        ws = WeekSchedule(3, MONDAY_DATE, 10.0)
        self.assertEqual("W3", ws.name())

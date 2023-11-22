# Generated by CodiumAI
import sys
from main import is_within_24_hours
from datetime import datetime, timedelta, date, timezone
from dateutil import parser



class TestIsWithin24Hours:

    # Returns True if the provided datetime is within the last 24 hours.
    def test_returns_true_within_last_24_hours(self):
        current_datetime = datetime.now()
        dt = current_datetime - timedelta(hours=23, minutes=59, seconds=59)
        assert is_within_24_hours(dt) is True

    # Returns False if the provided datetime is exactly 24 hours ago.
    def test_returns_false_exactly_24_hours_ago(self):
        current_datetime = datetime.now()
        dt = current_datetime - timedelta(hours=24)
        assert is_within_24_hours(dt) is False

    # Returns True if the provided datetime is less than 24 hours ago.
    def test_returns_false_less_than_24_hours_ago(self):
        current_datetime = datetime.now()
        dt = current_datetime - timedelta(hours=23, minutes=59, seconds=58)
        assert is_within_24_hours(dt) is True

    # Returns False if the provided datetime is exactly 25 hours ago.
    def test_returns_false_exactly_25_hours_ago(self):
        current_datetime = datetime.now()
        dt = current_datetime - timedelta(hours=25)
        assert is_within_24_hours(dt) is False

    # Returns False if the provided datetime is exactly 1 day and 1 second ago.
    def test_returns_false_exactly_1_day_and_1_second_ago(self):
        current_datetime = datetime.now()
        dt = current_datetime - timedelta(days=1, seconds=1)
        assert is_within_24_hours(dt) is False

    # Returns False if the provided datetime is exactly 1 day ago.
    def test_returns_false_exactly_1_day_ago(self):
        current_datetime = datetime.now()
        dt = current_datetime - timedelta(days=1)
        assert is_within_24_hours(dt) is False
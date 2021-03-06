import datetime

from django.utils import timezone
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from models import Election


# Create your tests here.
class ElectionMethodTests(TestCase):

    def test_in_election_window_with_future_election(self):
        """
        in_election_window() should return False for elections that
        have a start_date in the future
        """
        start_time = timezone.now() + datetime.timedelta(days=30)
        end_time = timezone.now() + datetime.timedelta(days=60)
        future_election = Election(start_date=start_time, end_date=end_time)
        self.assertEqual(future_election.in_election_window(), False)

    def test_in_electon_window_with_old_election(self):
        """
        in_election_window() should return False for elections that
        have a end_date in the past
        """
        start_time = timezone.now() - datetime.timedelta(days=60)
        end_time = timezone.now() - datetime.timedelta(days=30)
        past_election = Election(start_date=start_time, end_date=end_time)
        self.assertEqual(past_election.in_election_window(), False)

    def test_in_election_window_with_current_election(self):
        """
        in_election_window() should return True for elections that
        have a start_date in the past and end_date in the future
        """
        start_time = timezone.now() - datetime.timedelta(days=30)
        end_time = timezone.now() + datetime.timedelta(days=30)
        current_election = Election(start_date=start_time, end_date=end_time)
        self.assertEqual(current_election.in_election_window(), True)

    def test_user_login(self):
        """
           This tests both the creation of a user and that user login   KS
        """
        self.client = Client()
        self.username = 'test'
        self.email = 'test@test.com'
        self.password = 'test'

        self.test_user = User.objects.create_user(self.username,
                                                  self.email,
                                                  self.password)
        login = self.client.login(username=self.username,
                                  password=self.password)
        self.assertEqual(login, True)

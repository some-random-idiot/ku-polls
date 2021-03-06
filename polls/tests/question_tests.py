"""KU Poll's test cases."""

import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from ..models import Question


class QuestionModelTests(TestCase):
    """Contain tests for the Question model."""

    def test_was_published_recently_with_unreleased_poll(self):
        """Return False for polls that has their start_date in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_poll = Question(start_date=time)
        self.assertIs(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_past_poll(self):
        """Return False for polls that has their start_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_poll = Question(start_date=time)
        self.assertIs(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        """Returns True for polls whose start_date is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_poll = Question(start_date=time)
        self.assertIs(recent_poll.was_published_recently(), True)

    def test_question_is_published_unpublished(self):
        """Returns False if current date is before the poll’s publication date."""
        time = timezone.now() + datetime.timedelta(hours=23, minutes=59, seconds=59)
        unpublished_poll = Question(start_date=time)
        self.assertIs(unpublished_poll.is_published(), False)

    def test_question_is_published_past(self):
        """Returns True if current date is after the poll’s publication date."""
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        published_poll = Question(start_date=time)
        self.assertIs(published_poll.is_published(), True)

    def test_question_is_published_now(self):
        """Returns True if current date is on the poll’s publication date."""
        time = timezone.now()
        published_poll = Question(start_date=time)
        self.assertIs(published_poll.is_published(), True)

    def test_can_vote_before_published(self):
        """Returns False if current date is before the poll’s publication date."""
        time = timezone.now() + datetime.timedelta(hours=23, minutes=59, seconds=59)
        published_poll = Question(start_date=time)
        self.assertIs(published_poll.can_vote(), False)

    def test_can_vote_in_period(self):
        """Returns True if current date is within the poll’s voting period."""
        time_start = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        time_end = timezone.now() + datetime.timedelta(hours=23, minutes=59, seconds=59)
        published_poll = Question(start_date=time_start, end_date=time_end)
        self.assertIs(published_poll.can_vote(), True)

    def test_can_vote_after_end_date(self):
        """Returns False if current date is after the poll’s voting end date."""
        time_start = timezone.now() - datetime.timedelta(days=2)
        time_end = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        published_poll = Question(start_date=time_start, end_date=time_end)
        self.assertIs(published_poll.can_vote(), False)


def create_poll(text, start, end):
    """Create a poll with the given `text` and days offset."""
    return Question.objects.create(text=text, start_date=start, end_date=end)


class QuestionIndexViewTests(TestCase):
    """Contain tests for the Index view."""

    def test_no_polls(self):
        """If no polls exist, an appropriate message will be displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_past_poll(self):
        """Polls with a start_date in the past are displayed on the index page."""
        create_poll("Past poll.", start=timezone.now() - datetime.timedelta(days=30),
                    end=timezone.now() - datetime.timedelta(days=10))
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Question: Past poll.>']
        )

    def test_future_poll(self):
        """Polls with a start_date in the future aren't displayed on the index page."""
        create_poll("Future poll.", start=timezone.now() + datetime.timedelta(days=30),
                    end=timezone.now() - datetime.timedelta(days=40))
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_future_poll_and_past_poll(self):
        """Even if both past and future polls exist, only past polls are displayed."""
        create_poll("Past poll.", start=timezone.now() - datetime.timedelta(days=30),
                    end=timezone.now() - datetime.timedelta(days=10))
        create_poll("Past poll.", start=timezone.now() + datetime.timedelta(days=30),
                    end=timezone.now() - datetime.timedelta(days=40))
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Question: Past poll.>']
        )

    def test_two_past_polls(self):
        """The polls index page may display multiple polls."""
        create_poll("Past poll 1.", start=timezone.now() - datetime.timedelta(days=30),
                    end=timezone.now() - datetime.timedelta(days=10))
        create_poll("Past poll 2.", start=timezone.now() - datetime.timedelta(days=10),
                    end=timezone.now() - datetime.timedelta(days=5))
        create_poll("Present Poll.", start=timezone.now(), end=timezone.now() + datetime.timedelta(days=5))
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Question: Present Poll.>', '<Question: Past poll 2.>', '<Question: Past poll 1.>']
        )


class QuestionDetailViewTests(TestCase):
    """Contain tests for the Detail view."""

    def test_future_poll(self):
        """The detail view of a poll with a start_date in the future results in a redirect."""
        future_poll = create_poll("Dummy 1", start=timezone.now() + datetime.timedelta(days=5),
                                  end=timezone.now() + datetime.timedelta(days=10))
        url = reverse('polls:detail', args=(future_poll.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_poll(self):
        """The detail view of a poll with a end date in the past results in a redirect."""
        past_poll = create_poll("Dummy 2", start=timezone.now() - datetime.timedelta(days=15),
                                end=timezone.now() - datetime.timedelta(days=10))
        url = reverse('polls:detail', args=(past_poll.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

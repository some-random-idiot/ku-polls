import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_unreleased_poll(self):
        """
        Returns False for polls that has their start_date in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_poll = Question(start_date=time)
        self.assertIs(future_poll.was_published_recently(), False)

    def test_was_published_recently_with_past_poll(self):
        """
        Returns False for polls that has their start_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_poll = Question(start_date=time)
        self.assertIs(old_poll.was_published_recently(), False)

    def test_was_published_recently_with_recent_poll(self):
        """
        Returns True for polls whose start_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_poll = Question(start_date=time)
        self.assertIs(recent_poll.was_published_recently(), True)

    def test_question_is_published_unpublished(self):
        """
        Returns False if current date is before the poll’s publication date.
        """
        time = timezone.now() + datetime.timedelta(hours=23, minutes=59, seconds=59)
        unpublished_poll = Question(start_date=time)
        self.assertIs(unpublished_poll.is_published(), False)

    def test_question_is_published_past(self):
        """
        Returns True if current date is after the poll’s publication date.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        published_poll = Question(start_date=time)
        self.assertIs(published_poll.is_published(), True)

    def test_question_is_published_now(self):
        """
        Returns True if current date is on the poll’s publication date.
        """
        time = timezone.now()
        published_poll = Question(start_date=time)
        self.assertIs(published_poll.is_published(), True)

    def test_can_vote_before_published(self):
        """
        Returns False if current date is before the poll’s publication date.
        """
        time = timezone.now() + datetime.timedelta(hours=23, minutes=59, seconds=59)
        published_poll = Question(start_date=time)
        self.assertIs(published_poll.can_vote(), False)

    def test_can_vote_in_period(self):
        """
        Returns True if current date is within the poll’s voting period.
        """
        time_start = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        time_end = timezone.now() + datetime.timedelta(hours=23, minutes=59, seconds=59)
        published_poll = Question(start_date=time_start, end_date=time_end)
        self.assertIs(published_poll.can_vote(), True)

    def test_can_vote_after_end_date(self):
        """
        Returns False if current date is after the poll’s voting end date.
        """
        time_start = timezone.now() - datetime.timedelta(days=2)
        time_end = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        published_poll = Question(start_date=time_start, end_date=time_end)
        self.assertIs(published_poll.can_vote(), False)


def create_poll(text, days):
    """
    Create a poll with the given `text` and published the
    given number of `days` offset to now (negative for polls published
    in the past, positive for polls that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(text=text, start_date=time, end_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_polls(self):
        """
        If no polls exist, an appropriate message will be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_past_poll(self):
        """
        Polls with a start_date in the past are displayed on the index page.
        """
        create_poll(text="Past poll.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Question: Past poll.>']
        )

    def test_future_poll(self):
        """
        Polls with a start_date in the future aren't displayed on the index page.
        """
        create_poll(text="Future poll.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_poll_list'], [])

    def test_future_poll_and_past_poll(self):
        """
        Even if both past and future polls exist, only past polls are displayed.
        """
        create_poll(text="Past poll.", days=-30)
        create_poll(text="Future poll.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Question: Past poll.>']
        )

    def test_two_past_polls(self):
        """
        The polls index page may display multiple polls.
        """
        create_poll(text="Past poll 1.", days=-30)
        create_poll(text="Past poll 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_poll_list'],
            ['<Question: Past poll 2.>', '<Question: Past poll 1.>']
        )


class QuestionDetailViewTests(TestCase):
    def test_future_poll(self):
        """
        The detail view of a poll with a start_date in the future returns a 404 not found.
        """
        future_poll = create_poll(text='Future poll.', days=5)
        url = reverse('polls:detail', args=(future_poll.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_poll(self):
        """
        The detail view of a poll with a start_date in the past displays the poll's text.
        """
        past_poll = create_poll(text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_poll.id,))
        response = self.client.get(url)
        self.assertContains(response, past_poll.text)

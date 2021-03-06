from django.test import TestCase
from polls.models import Question
from django.utils import timezone
import datetime


class QuestionModelTests(TestCase):
    """ Test the question model """
    
    def test_was_published_recently_with_future_question(self):
        """ return False if the question published in the future """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """ return False if the question published in the past  """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """ return true if the question published recently """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """ return False if the current time is before the question was published """
        time = timezone + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with__old_question(self):
        """ return True if the current time is after the question was published """
        time = timezone.now() - datetime.timedelta(days=1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.is_published, True)

    def test_is_published_with__recent_question(self):
        """ return Ture if the current time is the time that the question was published """
        time = timezone.now() 
        old_question = Question(pub_date = time)
        self.assertIs(old_question.is_published, True)

    def test_can_vote_before_pub_date(self):
        """ return False that can vote before the question was published """
        pub_date = timezone.now() - datetime.timezone(days=1)
        question_before = Question(pub_date = pub_date, end_date = timezone.now())
        self.assertIs(question_before.can_vote(), False)

    def test_can_vote_at_pub_date(self):
        """ return True that can vote when the question was published """
        end_date = timezone.now() + datetime.timedelta(days=3)
        question = Question(pub_date = timezone.now() , end_date = end_date)
        self.assertIs(question.can_vote(), True)

    def test_can_vote_between_pub_date_and_end_date(self):
        """ return True that vote between published date and end date """
        pub_date = timezone.now() - datetime.timedelta(days=1)
        end_date = timezone.now() + datetime.timedelta(days=5)
        question = Question(pub_date = pub_date, end_date = end_date)
        self.assertIs(question.can_vote(), True)

    def test_can_vote_at_end_date(self):
        """ return False that vote at the end date of question """
        pub_date = timezone.now() + datetime.timedelta(days=3)
        question = Question(pub_date = pub_date, end_date = timezone.now())
        self.assertIs(question.can_vote(), False)

    def test_can_vote_after_end_date(self):
        """ return False that vote after the end date of question """
        pub_date = timezone.now()
        end_date = timezone.now() - datetime.timedelta(days=2)
        question = Question(pub_date = pub_date, end_date = end_date)
        self.assertIs(question.can_vote(), False)

def create_question(question_text, days):
    """ Create the question for polls app """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

from django.test import TestCase
import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from .models import Question

class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        time = timezone + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with__old_question(self):
        time = timezone.now() - datetime.timedelta(days=1)
        old_question = Question(pub_date = time)
        self.assertIs(old_question.is_published, True)

    def test_is_published_with__recent_question(self):
        time = timezone.now() 
        old_question = Question(pub_date = time)
        self.assertIs(old_question.is_published, True)

    def test_can_vote_before_pub_date(self):
        pub_date = timezone.now() - datetime.timezone(days=1)
        question_before = Question(pub_date = pub_date, end_date = timezone.now())
        self.assertIs(question_before.can_vote(), False)

    def test_can_vote_at_pub_date(self):
        end_date = timezone.now() + datetime.timedelta(days=3)
        question = Question(pub_date = timezone.now() , end_date = end_date)
        self.assertIs(question.can_vote(), True)

    def test_can_vote_between_pub_date_and_end_date(self):
        pub_date = timezone.now() - datetime.timedelta(days=1)
        end_date = timezone.now() + datetime.timedelta(days=5)
        question = Question(pub_date = pub_date, end_date = end_date)
        self.assertIs(question.can_vote(), True)

    def test_can_vote_at_end_date(self):
        pub_date = timezone.now() + datetime.timedelta(days=3)
        question = Question(pub_date = pub_date, end_date = timezone.now())
        self.assertIs(question.can_vote(), False)

    def test_can_vote_after_end_date(self):
        pub_date = timezone.now()
        end_date = timezone.now() - datetime.timedelta(days=2)
        question = Question(pub_date = pub_date, end_date = end_date)
        self.assertIs(question.can_vote(), False)

class QuestionIndexViewTests(TestCase):

    def test_no_question(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])


    def test_past_question(self):
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])
    
    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question.>'])

    def test_two_past_questions(self):
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],['<Question: Past question 2.>', '<Question: Past question 1.>'])

class QuestionDetailViewTests(TestCase):

    def test_future_question(self):
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

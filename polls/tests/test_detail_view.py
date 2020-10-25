from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import datetime
from polls.models import Question

class QuestionDetailViewTests(TestCase):
    """ Test the question detail view """

    def test_future_question(self):
        """ Test that return 404 not found if the question will published in the future """
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """ Test that display the question if the question was published """
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

def create_question(question_text, days):
    """ Create the question for polls app """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
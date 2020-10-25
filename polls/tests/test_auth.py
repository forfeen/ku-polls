from django.test import TestCase
from django.contrib.auth.models import User
from polls.models import Choice, Question
from django.utils import timezone
import datetime
from django.urls import reverse


class AuthTest(TestCase):
    """ Test authentication"""

    def setUp(self):
        self.q1 = create_question("Yes or No?", days=-1)
        self.c1 = Choice.objects.create(choice_text="Yes", question=self.q1)
        self.c2 = Choice.objects.create(choice_text="No", question=self.q1)
        self.username = "user"
        self.userpass = "1234"
        self.user = User.objects.create_user(self.username,password=self.userpass)
    
    def test_user_logged_in(self):
        """ Test that user can login """
        login_url = reverse('login')
        response = self.client.post(login_url, {'username': self.username, 'password': self.userpass})
        self.assertEqual(response.status_code, 302)
    
    def test_vote_requires_auth_user(self):
        """Test that user must be authenticated to vote. """
        try:
            self.client.logout(self)
        except Exception:
            pass

        vote_url = reverse('polls:vote', args=[self.q1.id])
        choice_id = self.q1.choice_set.first().id
        response = self.client.post( vote_url, {'choice':choice_id})
        self.assertEqual(response.status_code, 302)
        expect_url = reverse('login') + '?next=' + vote_url
        self.assertRedirects(response, expect_url)

        response = self.client.post( reverse('login'),
                    {'username':self.user.username, 'password':self.userpass})
        response = self.client.post( vote_url, {'choice':str(choice_id)})
        self.assertEqual(response.status_code, 302)
        expect_url = reverse('polls:results', args=[self.q1.id])
        self.assertRedirects(response, expect_url)
    


def create_question(question_text, days):
    """ Create the question for polls app """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)
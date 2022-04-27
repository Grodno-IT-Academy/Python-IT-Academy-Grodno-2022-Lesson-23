import datetime
# django utils
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
# model objects
from .models import Question

def create_question(question_text, days):
    # creates question with given text and time
    time = timezone.now() + datetime.timedelta(days=days)
    q = Question(question_text= question_text, pub_date=time)
    q.save()
    return q

class QuestionModelTests(TestCase):
    def test_no_questions(self):
        # testing a database free of questions
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls avaliable.')
        self.assertQuerysetEqual(response.context['questions_list'], [])
    def test_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Past question.')
        self.assertQuerysetEqual(response.context['questions_list'], [question])
    def test_future_quesiton(self):
        create_question(question_text='Future quesiton.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls avaliable.')
        self.assertNotContains(response, 'Future quesiton.')
        self.assertQuerysetEqual(response.context['questions_list'], [])
    def test_future_question_and_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text='Future quesiton.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Past question.')
        self.assertNotContains(response, 'Future quesiton.')
        self.assertQuerysetEqual(response.context['questions_list'], [question])
    def test_two_past_questions(self):
        question1 = create_question("Past question 1.", days=-1)
        question2 = create_question('Past question 2.', days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Past question 1.')
        self.assertContains(response, 'Past question 2.')
        self.assertQuerysetEqual(response.context['questions_list'], [question1, question2])


    def test_was_published_recently_with_future_question(self):
        # expecting false for future published question
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False, msg="Future question is not returning false for was_published_recently() method.")
    def test_was_published_recently_with_old_question(self):
        # expecting false for old question with pub date older than 1 day
        time = timezone.now() + datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
    def test_was_published_recently_with_recent_question(self):
        # expecting true for recent question with pub date younger than 1 day
        time = timezone.now() + datetime.timedelta(hours=-23, minutes=-59, seconds=-59)
        recent_question = Question(pub_date = time)
        self.assertIs(recent_question.was_published_recently(), True)
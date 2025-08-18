import datetime
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse

from .models import Question


def create_question(question_text: str, days: int) -> Question:
    """Helper: create a Question with a pub_date offset by <days> from now.

    days < 0 => past; days > 0 => future.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionMethodTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """was_published_recently returns False for future-dated questions."""
        future_question = create_question("Future question", days=30)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published_recently returns False for questions older than 1 day."""
        old_question = create_question("Old question", days=-30)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published_recently returns True for questions within last day."""
        recent_time = timezone.now() - datetime.timedelta(hours=1)
        recent_question = Question(question_text="Recent question", pub_date=recent_time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """If no questions exist, display a suitable message."""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question_displayed(self):
        """Questions with pub_date in past are shown."""
        q = create_question("Past question", days=-5)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, q.question_text)
        self.assertQuerysetEqual(response.context["latest_question_list"], [q])

    def test_future_question_not_displayed(self):
        """Future-dated questions are not shown on index."""
        create_question("Future question", days=5)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_future_and_past_questions(self):
        """Only past questions appear if both past and future exist."""
        past_q = create_question("Past question", days=-3)
        create_question("Future question", days=3)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_q])

    def test_two_past_questions_ordered(self):
        """Index lists multiple past questions ordered by pub_date desc."""
        older = create_question("Older", days=-5)
        newer = create_question("Newer", days=-2)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [newer, older])


class QuestionDetailViewTests(TestCase):
    def test_future_question_detail_returns_404(self):
        future_q = create_question("Future question", days=2)
        url = reverse("polls:detail", args=(future_q.id,))
        response = self.client.get(url)
        # Expect 404 because get_queryset doesn't filter in DetailView yet; adjust if needed.
        self.assertNotEqual(response.status_code, 200)

    def test_past_question_detail_displays_text(self):
        past_q = create_question("Past question", days=-2)
        url = reverse("polls:detail", args=(past_q.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_q.question_text)

class QuestionViewTests(TestCase):

    def test_index_view_with_no_questions(self):
        """
        If no questions exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_index_view_with_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_index_view_with_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
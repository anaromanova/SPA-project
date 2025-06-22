from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from spa_project.materials.models import Course, Subscription


class SubscriptionAPITestCase(APITestCase):

    def setUp(self):
        User = get_user_model()

        self.user = User.objects.create(email='joe@example.com')
        self.other = User.objects.create(email='anna@example.com')
        self.course = Course.objects.create(
                        title = 'Test Course',
                        description = 'Без ссылок',
                        user = self.other
                        )

    def test_subscribe_and_unsubscribe_flow(self):
        url_sub   = reverse('course-subscribe',   kwargs={'course_id': self.course.id})
        url_unsub = reverse('course-unsubscribe', kwargs={'course_id': self.course.id})

        resp = self.client.post(url_sub)
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.user)
        resp = self.client.post(url_sub)
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

        resp = self.client.post(url_sub)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

        resp = self.client.get(reverse('course-list'))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        body = resp.json()
        courses = body.get('results', [])
        data = {c['id']: c for c in courses}
        self.assertTrue(data[self.course.id]['is_subscribed'])

        resp = self.client.delete(url_unsub)
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())

        resp = self.client.delete(url_unsub)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_is_subscribed_false_for_anonymous_and_other(self):
        resp = self.client.get(reverse('course-list'))
        body = resp.json()
        courses = body.get('results', [])
        self.assertFalse(courses[0]['is_subscribed'])

        self.client.force_authenticate(self.other)
        resp = self.client.get(reverse('course-list'))
        body = resp.json()
        courses = body.get('results', [])
        self.assertFalse(courses[0]['is_subscribed'])

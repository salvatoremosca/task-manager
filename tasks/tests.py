from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from tasks.models import Task

User = get_user_model()


class TaskAPITests(APITestCase):
    '''
    Basic CRUD and authentication tests for Task API.

    TODO:
        Extend this test suite with additional cases as needed to achieve full coverage 
        and thoroughly validate all Task API functionalities.
    '''

    def setUp(self):

        # admin user
        self.admin_user = User.objects.create_superuser(
            username='admin', password='admin')

        # user 1
        self.normal_user_1 = User.objects.create_user(
            username='user1', password='user1')

        # user 2
        self.normal_user_2 = User.objects.create_user(
            username='user2', password='user2')

        # task 1 - admin
        self.t1_admin = Task.objects.create(
            owner=self.admin_user,
            title='t1-admin',
            status=Task.Status.PENDING
        )
        # task 1 - user 1
        self.t1_u1 = Task.objects.create(
            owner=self.normal_user_1,
            title='t1-user1',
            status=Task.Status.PENDING
        )
        # task 1 - user 2
        self.t1_u2 = Task.objects.create(
            owner=self.normal_user_2,
            title='t1-user2',
            status=Task.Status.DONE
        )
        # task 2 - user 2
        self.t2_u2 = Task.objects.create(
            owner=self.normal_user_2,
            title='t2-user2',
            status=Task.Status.IN_PROGRESS
        )
        self.list_url = '/api/tasks/'

    def test_requires_authentication(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_sees_only_own_tasks(self):
        self.client.force_authenticate(self.normal_user_1)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = {task['title'] for task in response.data}
        self.assertEqual(titles, {'t1-user1'})

    def test_admin_sees_all_tasks(self):
        self.client.force_authenticate(self.admin_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = {task['title'] for task in response.data}
        self.assertEqual(
            titles, {'t1-admin', 't1-user1', 't1-user2', 't2-user2'})

    def test_create_sets_owner_and_ignores_payload_owner(self):
        self.client.force_authenticate(self.normal_user_1)
        payload = {
            'title': 't2-user1',
            'status': Task.Status.PENDING,
            'owner': 'user2'}
        response = self.client.post(self.list_url, data=payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['owner'], 2)
        self.assertTrue(Task.objects.filter(
            owner=self.normal_user_1, title='t2-user1').exists())

    def test_patch_own_task(self):
        self.client.force_authenticate(self.normal_user_2)
        url = f'{self.list_url}{self.t1_u2.id}/'
        response = self.client.patch(
            url, data={'title': 't1-user2-edit'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.t1_u2.refresh_from_db()
        self.assertEqual(self.t1_u2.title, 't1-user2-edit')

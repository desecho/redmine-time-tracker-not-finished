# -*- coding: utf-8 -*-

import json

from bs4 import BeautifulSoup
from django.contrib.auth import get_user_model
from django.test import TestCase


class BaseTestCase(TestCase):
    fixtures = [
        'users.json',
    ]

    USER_PWD = 'password'
    # Superuser - admin/adminpassword
    # User - neo/password

    @staticmethod
    def get_soup(response):
        return BeautifulSoup(response.content)

    @staticmethod
    def get_json(response):
        return json.loads(response.content.decode('utf-8'))

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.get(username='neo')

    def login(self, username='neo'):
        self.client.logout()
        self.client.login(
            username=username,
            password=self.USER_PWD
        )


class BaseTestLoginCase(BaseTestCase):
    def setUp(self):
        super(BaseTestLoginCase, self).setUp()
        self.login()

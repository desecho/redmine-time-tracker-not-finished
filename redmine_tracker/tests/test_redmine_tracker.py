# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse

from .base import BaseTestLoginCase


class RedmineTrackerTestCase(BaseTestLoginCase):
    def test_home_view(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertIn('You need to enter your API key.', response.content.decode())

        # soup = self.get_soup(response)
        # self.assertTrue(soup.find('input', id='id_task_id'))

# encoding: utf-8
from __future__ import unicode_literals, print_function

import json
import unittest
import responses

from dynatademand.api import DemandAPIClient

BASE_HOST = "http://test-url.example"


class TestCategoryEndpoints(unittest.TestCase):
    def setUp(self):
        self.api = DemandAPIClient(client_id='test', username='testuser', password='testpass', base_host=BASE_HOST)
        self.api._access_token = 'Bearer testtoken'

    @responses.activate
    def test_get_survey_topics(self):
        with open('./tests/test_files/get_survey_topics.json', 'r') as survey_topics_file:
            survey_topics_json = json.load(survey_topics_file)
        responses.add(
            responses.GET,
            '{}/sample/v1/categories/surveyTopics'.format(BASE_HOST),
            json=survey_topics_json,
            status=200)
        self.api.get_survey_topics()
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(responses.calls[0].response.json(), survey_topics_json)

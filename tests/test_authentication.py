# encoding: utf-8
from __future__ import unicode_literals, print_function

import unittest
import responses

from dynatademand.api import DemandAPIClient
from dynatademand.errors import DemandAPIError

BASE_URL = "http://test-url.example"


class AuthenticationTestMissingCredentials(unittest.TestCase):
    def test_authentication_params(self):
        DemandAPIClient(client_id="test", username="test", password="test", base_host=BASE_URL)

        with self.assertRaises(DemandAPIError):
            DemandAPIClient(username="test", password="test", base_host=BASE_URL)

        with self.assertRaises(DemandAPIError):
            DemandAPIClient(client_id="test", password="test", base_host=BASE_URL)

        with self.assertRaises(DemandAPIError):
            DemandAPIClient(client_id="test", username="test", base_host=BASE_URL)


def api_test_url(endpoint):
    return "{}{}".format(BASE_URL, endpoint)


class AuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.client = DemandAPIClient(
            client_id="test_client_id",
            username="test_username",
            password="test_password",
            base_host=BASE_URL
        )
        self.assertEqual(self.client.client_id, "test_client_id")
        self.assertEqual(self.client.username, "test_username")
        self.assertEqual(self.client.password, "test_password")
        self.assertEqual(self.client.base_host, BASE_URL)

    @responses.activate
    def test_authenticate(self):
        responses.add(
            responses.POST,
            "{}{}".format(self.client.auth_base_url, "/token/password"),
            json={
                "accessToken": "access_token",
                "refreshToken": "refresh_token"
            }
        )
        self.client.authenticate()
        self.assertEqual(self.client._access_token, "access_token")
        self.assertEqual(self.client._refresh_token, "refresh_token")
        self.assertIsNone(self.client._check_authentication())

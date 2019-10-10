import os
import requests
from .errors import DemandAPIError


class DemandAPI(object):
    def __init__(self):
        self.client_id = os.getenv('DYNATA_DEMAND_CLIENT_ID', None)
        self.username = os.getenv('DYNATA_DEMAND_USERNAME', None)
        self.password = os.getenv('DYNATA_DEMAND_PASSWORD', None)
        if None in [self.client_id, self.username, self.password]:
            raise DemandAPIError("All authentication data is required.")
        self._access_token = None
        self.base_host = os.getenv('DYNATA_DEMAND_BASE_URL', 'https://api.researchnow.com')
        self.auth_base_url = '{}/auth/v1'.format(self.base_host)
        self.base_url = '{}/sample/v1'.format(self.base_host)

    def _check_authentication(self):
        if self._access_token is None:
            raise DemandAPIError('The API instance must be authenticated before calling this method.')

    def authenticate(self):
        url = '{}/token/password'.format(self.auth_base_url)
        payload = {
            'clientId': self.client_id,
            'password': self.password,
            'username': self.username,
        }
        auth_response = requests.post(url, json=payload)
        if auth_response.status_code > 399:
            raise DemandAPIError('Authentication failed with status {} and error: {}'.format(
                auth_response.status_code,
                auth_response.json())
            )
        self._access_token = auth_response.json().get('accessToken')
        return self._access_token

    def api_call(self, uri, method, payload):
        self._check_authentication()
        url = '{}{}'.format(self.base_url, uri)
        response = requests.request(url=url, method=method, json=payload, headers={'oauth_access_token': self._access_token})
        if response.status_code > 399:
            raise DemandAPIError('Demand API request failed with status {}. Response: {}'.format(response.status_code, response.json()))
        return response.json()

import json
import logging
import re
from datetime import datetime
from json import JSONDecodeError
from typing import List

import requests

from .Config import APIConfig
from .Exceptions import AuthException, ApiException
from .utils.helper import update_file

logger = logging.getLogger("pydisney")
logger = logger.getChild("Auth")


class Auth:
    def __init__(self, email, password, force_login):
        self._email = email
        self._force_login = force_login
        self._password = password
        self._web_page = 'https://www.disneyplus.com/login'
        self._devices_url = "https://disney.api.edge.bamgrid.com/devices"
        self._login_url = 'https://disney.api.edge.bamgrid.com/idp/login'
        self._token_url = "https://disney.api.edge.bamgrid.com/token"
        self._grant_url = 'https://disney.api.edge.bamgrid.com/accounts/grant'

        APIConfig.auth = self

    def _client_api_key(self):
        res = APIConfig.session.get(self._web_page)
        match = re.search("window.server_path = ({.*});", res.text)
        janson = json.loads(match.group(1))
        clientapikey = janson["sdk"]["clientApiKey"]
        return clientapikey

    def _assertion(self, client_apikey):

        postdata = {
            "applicationRuntime": "firefox",
            "attributes": {},
            "deviceFamily": "browser",
            "deviceProfile": "macosx"
        }

        header = {"authorization": f"Bearer {client_apikey}", "Origin": "https://www.disneyplus.com"}
        res = APIConfig.session.post(url=self._devices_url, headers=header, json=postdata)

        if not res.ok:
            raise AuthException(res)

        assertion = res.json()["assertion"]

        return assertion

    def _access_token(self, client_apikey, assertion):

        header = {"authorization": f"Bearer {client_apikey}", "Origin": "https://www.disneyplus.com"}

        post_date = {
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "latitude": "0",
            "longitude": "0",
            "platform": "browser",
            "subject_token": assertion,
            "subject_token_type": "urn:bamtech:params:oauth:token-type:device"
        }

        res = APIConfig.session.post(url=self._token_url, headers=header, data=post_date)

        if not res.ok:
            raise AuthException(res)

        access_token = res.json()["access_token"]
        return access_token

    def _login(self, access_token):
        headers = {
            'accept': 'application/json; charset=utf-8',
            'authorization': "Bearer {}".format(access_token),
            'content-type': 'application/json; charset=UTF-8',
            'Origin': 'https://www.disneyplus.com',
            'Referer': 'https://www.disneyplus.com/login/password',
            'Sec-Fetch-Mode': 'cors',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'x-bamsdk-platform': 'windows',
            'x-bamsdk-version': '3.10',
        }

        data = {'email': self._email, 'password': self._password}
        res = APIConfig.session.post(url=self._login_url, data=json.dumps(data), headers=headers)

        if not res.ok:
            raise AuthException(res)

        id_token = res.json()["id_token"]
        return id_token

    def _grant(self, id_token, access_token):

        headers = {
            'accept': 'application/json; charset=utf-8',
            'authorization': f"Bearer {access_token}",
            'content-type': 'application/json; charset=UTF-8',
            'Origin': 'https://www.disneyplus.com',
            'Referer': 'https://www.disneyplus.com/login/password',
            'Sec-Fetch-Mode': 'cors',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36',
            'x-bamsdk-platform': 'windows',
            'x-bamsdk-version': '3.10',
        }

        data = {'id_token': id_token}

        res = APIConfig.session.post(url=self._grant_url, data=json.dumps(data), headers=headers)

        if not res.ok:
            raise AuthException(res)

        assertion = res.json()["assertion"]

        return assertion

    def _final_token(self, subject_token, client_apikey):

        header = {"authorization": f"Bearer {client_apikey}", "Origin": "https://www.disneyplus.com"}

        postdata = {
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "latitude": "0",
            "longitude": "0",
            "platform": "browser",
            "subject_token": subject_token,
            "subject_token_type": "urn:bamtech:params:oauth:token-type:account"
        }

        res = APIConfig.session.post(url=self._token_url, headers=header, data=postdata)

        if not res.ok:
            raise AuthException(res)
        access_token = res.json()["access_token"]
        expires_in = res.json()["expires_in"]
        refresh_token = res.json()["refresh_token"]

        return access_token, expires_in, refresh_token

    def _get_auth_token_tru_api(self):
        logger.info("Loging using disney's api")
        logger.warning("Loging using Disney's api repeatedly will cause account blocks")
        clientapikey_ = self._client_api_key()
        assertion_ = self._assertion(clientapikey_)

        access_token_ = self._access_token(clientapikey_, assertion_)
        id_token_ = self._login(access_token_)

        user_assertion = self._grant(id_token_, access_token_)
        token, expire, refresh = self._final_token(user_assertion, clientapikey_)

        APIConfig.token = token
        APIConfig.refresh = refresh
        update_file()

    @staticmethod
    def refreshToken():
        with open("token.json", "r", encoding="utf8") as file:
            data = json.load(file)

            refresh = data["refresh"]

            logger.info("Refreshing access token using refresh token from token.json file")
            graph_mutation = {
                "query": "mutation refreshToken($input:RefreshTokenInput!){refreshToken(refreshToken:$input){activeSession{sessionId}}}",
                "variables": {
                    "input": {
                        "refreshToken": refresh
                    }
                },
                "operationName": "refreshToken"
            }
            res = APIConfig.session.post(url="https://disney.api.edge.bamgrid.com/graph/v1/device/graphql",
                                         json=graph_mutation,
                                         headers={"authorization": APIConfig.auth._client_api_key()})
            if not res.ok:
                raise AuthException(res)

            if not res.json()["data"]:
                errors = []
                for error in res.json()["errors"]:
                    errors.append(error)
                logger.info("Couldn't refresh access token with refresh token:\n%s", errors)
                #  trying one last time to get access token via standard login procedure using email and password
                APIConfig.auth._get_auth_token_tru_api()
                return

            res_json = res.json()

            APIConfig.token = res_json["extensions"]["sdk"]["token"]["accessToken"]
            APIConfig.refresh = res_json["extensions"]["sdk"]["token"]["refreshToken"]
            update_file()

    @staticmethod
    def make_request(method: str, url: str, data: dict = None, headers: dict = None, params: dict = None, files: dict = None) -> dict:
        logger.debug(f"Calling... Url={url}, Method={method}, Headers={headers}")
        default_headers = {
            'accept': 'application/vnd.media-service+json; version=6',
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
            'x-bamsdk-platform': "macOS",
            'x-bamsdk-version': '23.1',
            'x-dss-edge-accept': 'vnd.dss.edge+json; version=2',
            'x-dss-feature-filtering': 'true',
            'Origin': 'https://www.disneyplus.com',
            'authorization': APIConfig.token
        }

        if params is None:
            params = {}

        if headers is None:
            headers = {}
        headers.update(default_headers)
        response = requests.request(method, url, headers=headers, json=data, params=params, files=files)

        if not response.ok:
            raise ApiException(response)

        if response.status_code == 200:
            return response.json()

    @staticmethod
    def make_pagination_request(method: str, url: str, data: dict = None, headers: dict = None, params: dict = None, files: dict = None) -> List[dict]:
        if params is None:
            params = {}
        params.setdefault('limit', 200)
        params.setdefault('offset', 0)

        aggregated_results = []
        current_offset = params['offset']
        limit = params['limit']

        while True:
            logger.debug(f"Fetching page with offset={current_offset}, limit={limit}")
            params['offset'] = current_offset

            # Use the existing make_request method
            response_json = Auth.make_request(
                method=method,
                url=url,
                data=data,
                headers=headers,
                params=params,
                files=files
            )

            from .utils.parser import find_pagination_values  # circular import
            pagination_values = find_pagination_values(response_json)

            logger.debug(f"Pagination Values: {pagination_values}")

            aggregated_results.append(response_json)

            # Check if there are more pages
            if pagination_values and pagination_values.get('hasMore', False):
                current_offset += limit
            else:
                break

        return aggregated_results

    @staticmethod
    def make_stream_request(url):
        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}

        res = APIConfig.session.get(url=url, headers=headers, stream=True, timeout=10)
        if res.status_code == 401:
            raise AuthException(res)
        if not res.ok:
            raise ApiException(res)

        return res

    def get_auth_token(self):
        if self._force_login:
            self._get_auth_token_tru_api()
            return
        try:
            with open("token.json", "r", encoding="utf8") as file:

                data = json.load(file)
                token = data["token"]
                refresh = data["refresh"]
                expiration_time_str = data["expiration_time"]

                # Convert the expiration time string back to a datetime object
                expiration_time = datetime.strptime(expiration_time_str, "%Y-%m-%d %H:%M:%S")

                # Check if the token is still valid
                current_time = datetime.now()
                if current_time < expiration_time:
                    logger.info("Authenticating using token from token.json file")

                    APIConfig.token = token
                    APIConfig.refresh = refresh
                else:
                    logger.info("Access token is expired, refreshing...")

                    self.refreshToken()

        except (FileNotFoundError, KeyError, JSONDecodeError):

            logger.info("Creating token.json file")
            open("token.json", "a+", encoding="utf8").close()

            self._get_auth_token_tru_api()

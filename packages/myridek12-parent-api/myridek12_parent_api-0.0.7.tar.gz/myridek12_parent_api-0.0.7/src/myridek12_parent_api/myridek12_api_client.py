"""MySchoolBucks Parent API Client."""
import logging

from urllib.parse import urljoin

import aiohttp
import base64
import hashlib
import html
import os
import re
import urllib
from bs4 import BeautifulSoup

from .errors import MyRideK12Error
from .models.base import StudentResponse,Address,BusRun,BusRunDetail,CustomField,BusStop

_LOGGER = logging.getLogger(__name__)
_LOGGER.setLevel(logging.INFO)

def _enable_debug_logging():
    _LOGGER.setLevel(logging.DEBUG)

class MyRideK12ApiClient():
    """MyRideK12 API Client"""
    def __init__(
        self,
        username,
        password,
        debug=False,
    ):
        if debug:
            _enable_debug_logging()
        
        self._redirect_uri   = 'https://myridek12.tylerapp.com/authentication/login-callback'
        self._username       = username
        self._password       = password
        self._login_provider = 'https://login.myridek12.tylerapp.com'
        self._api_provider   = 'https://myridek12.tylerapi.com/'
        self._access_token   = None
        self._refresh_token  = None
        self._client_id      = '3c5382gsq7g13djnejo98p2d98'

        self._code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
        self._code_verifier = re.sub('[^a-zA-Z0-9]+', '', self._code_verifier)
        self._code_verifier, len(self._code_verifier)

        self._code_challenge = hashlib.sha256(self._code_verifier.encode('utf-8')).digest()
        self._code_challenge = base64.urlsafe_b64encode(self._code_challenge).decode('utf-8')
        self._code_challenge = self._code_challenge.replace('=', '')
        self._code_challenge, len(self._code_challenge)

        self._nonce = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')
        self._state = base64.urlsafe_b64encode(os.urandom(40)).decode('utf-8')

    async def get_token(self, session) -> str:
        """Test if we can get a token from the MyRideK12 API"""
        try:
            request_url = urljoin(
                self._login_provider,(f"/oauth2/authorize")
            )

            params={
                "response_type": "code",
                "client_id": self._client_id,
                "scope": "openid email phone profile aws.cognito.signin.user.admin",
                "redirect_uri": self._redirect_uri,
                "state": self._state,
                "code_challenge": self._code_challenge,
                "code_challenge_method": "S256",
                "code_verifier": self._code_verifier
            }

            auth_code = None

            async with session.get(request_url,params=params) as authorization:
                response = authorization
                responsetext = await response.text()

                form_action = html.unescape(re.search('<form\s+.*?\s+action="(.*?)"', responsetext, re.DOTALL).group(1))
                parsed_html = BeautifulSoup(responsetext, 'html.parser')
                hidden_tags = parsed_html.find_all("input", type="hidden")
                csrf = hidden_tags[0]['value']

                data = {
                    '_csrf' : csrf,
                    'username' : self._username,
                    'password' : self._password
                }
                login_url = self._login_provider+form_action

                async with session.post(login_url,data=data,allow_redirects=False) as login:
                    response = login
                    redirect = response.headers['Location']

                    query = urllib.parse.urlparse(redirect).query
                    redirect_params = urllib.parse.parse_qs(query)

                    auth_code = redirect_params['code'][0]

                    token_url = self._login_provider+"/oauth2/token"
                    data = {
                        "grant_type": "authorization_code",
                        "client_id": self._client_id,
                        "code": auth_code,
                        "redirect_uri": self._redirect_uri,
                        "code_verifier": self._code_verifier
                    }
                    async with session.post(token_url,data=data,allow_redirects=False) as token:
                        response = token
                        token = await response.json()
                        self._access_token = token['access_token']
                        self._refresh_token = token['refresh_token']
                        
                        return self._access_token

        except Exception as error:
            raise MyRideK12Error(400, error)
        
    async def _get_request(self, end_url: str) -> dict:
        """Perform GET request to API endpoint."""
        request_url = urljoin(self._api_provider, end_url)

        async with aiohttp.ClientSession() as session:
            token = await self.get_token(session)
            if token:
                headers = {
                    "Authorization": f"Bearer {token}",
                    'x-tenant-id': '4dc8ef3a-6f22-430c-a9e1-1101c0366d2e'
                }
                async with session.get(f"{request_url}", headers=headers) as resp:
                    response = resp
                    responsetext = await resp.text()
                    response_json = await resp.json()
                    if response.status >= 400:
                        raise MyRideK12Error(response.status, responsetext)
                    return response_json
            raise MyRideK12Error(400, "Bad Credentials")
        

    async def get_students(self) -> list[StudentResponse]:
        """Get Students from MyRideK12"""
        parsed_response = await self._get_request("/api/student")
        if parsed_response:
            studentresp: list[StudentResponse] = [StudentResponse(**resp) for resp in parsed_response]
            return studentresp
        return []
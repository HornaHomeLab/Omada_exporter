from dataclasses import dataclass, field
import os
import requests
from requests.cookies import RequestsCookieJar

@dataclass
class UserSession:
    username: str = field(init=True)
    password: str = field(init=True)
    omada_cid: str = field(init=True)
    
    session: requests.Session = field(init=False)

    __base_url: str = field(init=False)
    __login_endpoint: str = field(init=False, default="{base_url}/{omadacId}/api/v2/login")
    __logout_endpoint: str = field(init=False, default="{base_url}/{omadacId}/api/v2/logout")

    def __post_init__(self):
        self.session = requests.Session()
        self.session.cookies = RequestsCookieJar()
        self.__base_url = os.getenv("BASE_URL")
        self.__login()

    def __del__(self):
        self.__logout()

    def __login(self):
        url = self.__login_endpoint.format(
            base_url=self.__base_url,
            omadacId=self.omada_cid
        )

        response = self.session.post(
            url,
            json={'username': self.username, 'password': self.password}
        )
        login_result = response.json()
        self.session.headers.update(
            {
                "Csrf-Token": login_result["result"]['token'],
            }
        )

    def __logout(self):
        url = self.__logout_endpoint.format(
            base_url=self.__base_url,
            omadacId=self.omada_cid
        )
        t = self.session.post(
            url
        )

        result = t.json()
        return result

    def get_session(self) -> requests.Session:
        return self.session


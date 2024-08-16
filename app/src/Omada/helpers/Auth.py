import os
from dotenv import load_dotenv
import datetime
import requests
import src.Omada.helpers.requestsResult as requestHelpers

load_dotenv()

class Auth:
    __client_id: str = os.getenv('OMADA_CLIENT_ID')
    __client_secret: str = os.getenv('OMADA_CLIENT_SECRET')
    __get_token_endpoint: str = "{base_url}/openapi/authorize/token?grant_type=client_credentials"
    __refresh_token_endpoint: str = "{base_url}/openapi/authorize/token?client_id={client_id}&client_secret={client_secret}&refresh_token={refresh_token}&grant_type=refresh_token"
    __api_info_endpoint: str = "{base_url}/api/info"
    __auth_access_token: str = None
    __auth_refresh_token: str = None
    __base_url: str = os.getenv("BASE_URL")
    
    expires_at: datetime.datetime = None
    omada_cid: str = None

    @staticmethod
    def get_token() -> str:
        if not Auth.__auth_access_token:
            Auth.__request_token()
            return Auth.__auth_access_token
        
        if not Auth.__is_token_expired():
            return Auth.__auth_access_token
        
        Auth.__refresh_token()
        return Auth.__auth_access_token
        
        
    
    @staticmethod
    def __is_token_expired() -> bool:
        return ((Auth.expires_at - datetime.timedelta(seconds=60)) > datetime.datetime.now())


        
    @staticmethod
    def __set_expiration_time(expires_in: int) -> None:
        
        Auth.expires_at = datetime.datetime.now() + datetime.timedelta(seconds=expires_in)
        
    @staticmethod
    def __request_token() -> None:
        url = Auth.__get_token_endpoint.format(
            base_url=Auth.__base_url
        )
        body= {
            "omadacId": Auth.omada_cid,
            "client_id": Auth.__client_id,
            "client_secret": Auth.__client_secret
        }
        response: requests.Response = requests.post(url=url,json=body)
        response: dict = requestHelpers.get_request_result(url,response)
        
        Auth.__auth_access_token = response.get("accessToken")
        Auth.__auth_refresh_token = response.get("refreshToken")
        Auth.__set_expiration_time(response.get("expiresIn"))
        
    @staticmethod
    def __refresh_token() -> None:
        url = Auth.__refresh_token_endpoint.format(
            base_url=Auth.__base_url,
            client_id=Auth.__client_id,
            client_secret=Auth.__client_secret,
            refresh_token=Auth.__auth_refresh_token
        )
        response: dict = requests.post(url)
        response: dict = requestHelpers.get_request_result(url,response)
        
        Auth.__auth_access_token = response.get("accessToken")
        Auth.__auth_refresh_token = response.get("refreshToken")
        Auth.__set_expiration_time(response.get("expiresIn"))
        
    
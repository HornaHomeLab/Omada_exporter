import os
from dotenv import load_dotenv
import requests
from src.Omada.helpers.Auth import Auth
import src.Omada.helpers.requestsResult as requestHelpers

load_dotenv()

class Request:

    site_id: str = None
    omada_cid: str = None
    controller_version: str = None
    api_version: str = None
    
    __base_url: str = os.getenv("BASE_URL")
    __verify_certificate: bool = os.getenv("VERIFY_CERTIFICATE")

    __page_size: int = 100

    @staticmethod
    def get(
        path: str, arguments: dict = {}, include_auth: bool = True, include_params: bool = True, page: int = 1
    ) -> dict:
        headers = Request.__get_headers(include_auth)
        params = Request.__get_params(page, include_params)

        url = Request.__get_url(path, arguments)
        response = requests.get(
            url,
            headers=headers,
            params=params,
            verify=Request.__verify_certificate
        )
        result: dict = requestHelpers.get_request_result(url, response)

        if Request.__has_data(result):
            if not Request.__has_more_data_to_fetch(result):
                return result.get("data")

            result = result.get("data")
            result += Request.get(
                path, include_auth, include_params, page+1
            )

        return result

    @staticmethod
    def post(path: str, body: dict = None):
        url = Request.__get_url(path)

        if body is not None:
            response = requests.post(
                url=url, json=body, verify=Request.__verify_certificate
            )
        else:
            response = requests.post(
                url=url, verify=Request.__verify_certificate)

        return requestHelpers.get_request_result(url, response)

    @staticmethod
    def __get_url(path: str, arguments: dict = {}) -> str:
        arguments = {
            "omadacId": Request.omada_cid,
            "siteId": Request.site_id,
            **arguments
        }
        path: str = path.format(
            **arguments
        )
        return "{base}{endpoint_path}".format(
            base=Request.__base_url,
            endpoint_path=path
        )

    @staticmethod
    def __get_headers(include_auth_headers: bool = True) -> dict:
        if include_auth_headers:
            return {
                "Authorization": "AccessToken={token}".format(
                    token=Auth.get_token()
                ),
                "content-type": "application/json"
            }
        return None

    @staticmethod
    def __get_params(page: int = 1, include_params: bool = True) -> dict:
        if include_params:
            return {
                "pageSize": Request.__page_size,
                "page": page
            }
        return None

    @staticmethod
    def __get_fetched_rows(result: dict) -> int:
        return result.get("currentPage") * result.get("currentSize")

    @staticmethod
    def __has_more_data_to_fetch(result: dict) -> bool:
        return (Request.__get_fetched_rows(result) < result.get("totalRows"))

    @staticmethod
    def __has_data(result: dict) -> bool:
        try:
            return ('data' in list(result.keys()))
        except:
            return False
        
    @staticmethod
    def init()->None:
        api_info = Request.get(
            "/api/info", include_auth=False, include_params=False
        )
        Request.controller_version = api_info.get("controllerVer")
        Request.api_version = api_info.get("apiVer")
        Request.omada_cid = api_info.get("omadacId")
        Auth.omada_cid = api_info.get("omadacId")

        site = Request.get("/openapi/v1/{omadacId}/sites")
        Request.site_id = [
            entry.get("siteId")
            for entry in site
            if entry.get("name") == os.getenv("SITE_NAME")
        ][0]

Request.init()
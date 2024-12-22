import hashlib
import time
import asyncio
from copy import deepcopy
from typing import Any, List, Literal, Optional
from pycrystalpay.exceptions import CrystalApiException

from httpx import AsyncClient


class BaseApiWrapper:
    """Poviding base api tools
    """
    API_ENDPOINT = "https://api.crystalpay.io/"
    API_VESION = "v3"
    __last_time_request = -1
    __requests_amount = 0
    __base_limit = 5

    def __init__(self, auth_login: str, auth_secret: str, salt: Optional[str]=None, wait_cooldown: bool=True, **kwargs):
        """

        Args:
            auth_login (str): merchant login
            auth_secret (str): merchant secret
            **kwrags: params will be passed to httpx.AsyncClient
        """

        self.__auth_login = auth_login
        self.__auth_secret = auth_secret
        self.__client = AsyncClient(**kwargs)
        self.__api_endpoint = self.API_ENDPOINT + self.API_VESION + '/'
        self.__salt = salt

        self.__wait_cooldown = wait_cooldown

    async def _cooldown_waiter(self):
        """Ожидание лимита

        About query limits: https://docs.crystalpay.io/#limity-api
        """

        if not self.__wait_cooldown:
            return
        now_second = int(time.time())
        if BaseApiWrapper.__last_time_request == now_second and\
             BaseApiWrapper.__requests_amount == BaseApiWrapper.__base_limit:
            # May be sleep in ms..
            await asyncio.sleep(1)
            BaseApiWrapper.__last_time_request = int(time.time())
            BaseApiWrapper.__requests_amount = 1
        elif BaseApiWrapper.__last_time_request != now_second:
            BaseApiWrapper.__requests_amount = 0
            BaseApiWrapper.__last_time_request = now_second
        BaseApiWrapper.__requests_amount += 1  

    async def _send_request(
        self,
        http_method: Literal["GET", "POST"],
        api_route: str,
        data: dict[str, Any]=None, #type: ignore
        provide_creds: bool=True,
        sign_values: List[str]=None #type: ignore
        ) -> dict:
        """Отправка запроса к апи

        Args:
            http_method (str): (GET, POST)
            api_route (str): ex(invoice/info)
            data (dict[str, Any]): json request data
            provide_creds (bool): should add login and secret to body

        Returns:
            dict: loaded json response
        """

        request_data = deepcopy(data)

        if provide_creds:
            if request_data is None:
                request_data = {}

            request_data.update(
                {
                    "auth_login": self.__auth_login,
                    "auth_secret": self.__auth_secret
                }
            )
        
        requested_data = {k: v for k, v in request_data.items() if v is not None}

        if not sign_values is None:
            sign = self.create_sign(to_sign=sign_values)
            requested_data["signature"] = sign

        await self._cooldown_waiter()
        response = await self.__client.request(
            http_method,
            self.__api_endpoint + api_route,
            json=requested_data
        )
        parsed_response = response.json()
        if parsed_response.get("error") is True:
            errors = parsed_response.get("errors")
            raise CrystalApiException('\n'.join(errors))
        return parsed_response

    def create_sign(self, to_sign: List[str]) -> str:
        """Создание подписи

        Doc - https://docs.crystalpay.io/specifikaciya/primery-po-rabote-s-api-na-raznykh-yazykakh#generaciya-podpisi-signature

        Args:
            *args: данные для включения в подпись в точном порядке
        Returns:
            Хеш
        """
        if not self.__salt:
            raise ValueError("`salt` не передан. Невозможно создать подпись.")
        
        sign_str = ':'.join([*to_sign, self.__salt])
        return hashlib.sha1(sign_str.encode()).hexdigest()
    
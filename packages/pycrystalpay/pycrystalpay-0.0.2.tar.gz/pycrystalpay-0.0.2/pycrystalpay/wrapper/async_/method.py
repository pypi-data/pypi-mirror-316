from typing import Any, Union
from pycrystalpay.types import MethodList, PAYMENT_METHODS, MethodGet

from .base import BaseApiWrapper


class Method(BaseApiWrapper):
    """Providing `method` methods

    Doc - https://docs.crystalpay.io/metody-api/method-metody
    """

    async def method_list(self, compact: bool=False) -> MethodList:
        """Getting methods list

        Doc - https://docs.crystalpay.io/metody-api/method-metody/poluchenie-spiska-metodov
        """
        data = await self._send_request(
            "POST",
            "method/list/",
            {
                "compact": compact
            }
        )
        return MethodList.model_validate(data)
   
    async def method_get(self, method: Union[PAYMENT_METHODS, str]) -> MethodGet:
        """Getting information about method

        Doc - https://docs.crystalpay.io/metody-api/method-metody/poluchenie-metoda
        """
        data = await self._send_request(
            "POST",
            "method/get/",
            {
                "method": method
            }
        )
        return MethodGet.model_validate(data)

    async def method_edit(self, method: Union[PAYMENT_METHODS, str], enabled: Union[bool, None]=None, extra_commission_percent: Union[int, None]=None) -> bool:
        """Edit information about method

        Doc - https://docs.crystalpay.io/metody-api/method-metody/izmenenie-nastroek-metoda
        """
        if enabled is None and extra_commission_percent is None:
            raise ValueError("`enabled` or `extra_commission_percent` must be provided!")

        data = await self._send_request(
            "POST",
            "method/get/",
            {
                "method": method,
                "enabled": enabled,
                "extra_commission_percent": extra_commission_percent
            }
        )
        return data.get("error", None) is False

from typing import Union
from pycrystalpay.types import BalanceGet, BalanceList, PAYMENT_METHODS

from .base import BaseApiWrapper


class Balance(BaseApiWrapper):
    """Методы `balance`

    Doc - https://docs.crystalpay.io/metody-api/balance-balansy
    """

    async def balance_list(self, hide_empty: bool=False) -> BalanceList:
        """Получить список методов и их балансов

        Doc - https://docs.crystalpay.io/metody-api/balance-balansy/poluchenie-spiska-balansov

        Args:
            hide_empty (bool) - скрыть пустые балансы
        """
        data = await self._send_request(
            "POST",
            "balance/list/",
            {
                "hide_empty": hide_empty
            }
        )
        return BalanceList.model_validate(data)

    async def balance_get(self, method: Union[PAYMENT_METHODS, str]) -> BalanceGet:
        """Получить баланс определенного метода

        Doc - https://docs.crystalpay.io/metody-api/balance-balansy/poluchenie-balansa

        Args:
            method (bool) - название метода
        """
        data = await self._send_request(
            "POST",
            "balance/get/",
            {
                "method": method
            }
        )
        return BalanceGet.model_validate(data)

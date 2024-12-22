from typing import Union, Optional
from pycrystalpay.types import PAYMENT_METHODS, SUBSTRUCT_FROM, PayoffCreate, PayoffSubmit

from .base import BaseApiWrapper


class Payoff(BaseApiWrapper):
    """Методы `payoff` 

    Doc - https://docs.crystalpay.io/metody-api/payoff-vyvody
    """

    async def payoff_create(
            self,
            method: Union[PAYMENT_METHODS, str],
            wallet: str,
            amount: int,
            subtract_from: SUBSTRUCT_FROM,
            amount_currency: Optional[str]=None,
            wallet_extra: Optional[str]=None,
            extra: Optional[str]=None,
            callback_url: Optional[str]=None
            ) -> PayoffCreate:
        """Создание вывода

        Doc - https://docs.crystalpay.io/metody-api/payoff-vyvody/sozdanie-vyvoda

        Args:
            method (Union[PAYMENT_METHODS, str]): Внутреннее название метода
            wallet (str): Реквизиты получателя
            amount (int): Сумма вывода
            subtract_from (SUBSTRUCT_FROM): Откуда вычитать комиссию
            amount_currency (str, optional): Валюта суммы. Defaults to None.
            wallet_extra (str, optional): Дополнительная информация о реквизитах получателя. Defaults to None.
            extra (str, optional): Любые данные, например ID вывода в вашей системе. Defaults to None.
            callback_url (str, optional): Ссылка для отправки http callback уведомления о выводе. Defaults to None.

        """
        data = await self._send_request(
            "POST",
            "payoff/create/",
            {
                "method": method,
                "wallet": wallet,
                "amount": amount,
                "subtract_from": subtract_from,
                "amount_currency": amount_currency,
                "wallet_extra": wallet_extra,
                "extra": extra,
                "callback_url": callback_url
                
            },
            sign_values=[str(amount), method, wallet]
        )
        return PayoffCreate.model_validate(data)
 
    async def payoff_submit(self, id_: str) -> PayoffSubmit:
        """Подтверждение вывода

        Doc - https://docs.crystalpay.io/metody-api/payoff-vyvody/podtverzhdenie-vyvoda

        Args:
            id (str): ID вывода
        """

        data = await self._send_request(
            "POST",
            "payoff/submit/",
            {
                "id": id_,
            },
            sign_values=[id_]
        )
        return PayoffSubmit.model_validate(data)

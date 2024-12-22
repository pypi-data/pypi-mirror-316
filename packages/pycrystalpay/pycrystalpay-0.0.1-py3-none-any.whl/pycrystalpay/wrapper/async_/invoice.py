import warnings
from typing import Union
from pycrystalpay.types import INVOICE_TYPES, PAYMENT_METHODS, InvoiceInfo, InvoiceCreate

from .base import BaseApiWrapper


class Invoice(BaseApiWrapper):
    """Методы `invoice` 
    Doc - https://docs.crystalpay.io/metody-api/invoice-platezhi
    """

    async def invoice_create(
            self,
            amount: int,
            type_: INVOICE_TYPES,
            lifetime: int,
            amount_currency: str=None, # type: ignore
            required_method: Union[PAYMENT_METHODS]=None, # type: ignore
            payer_details: str=None, # type: ignore
            description: str=None, # type: ignore
            extra: str=None, # type: ignore
            redirect_url: str=None, # type: ignore
            callback_url: str = None # type: ignore


        ) -> InvoiceCreate:
        """Создание платежа

        Args:
            amount (int): Сумма к оплате
            type (INVOICE_TYPES): Тип инвойса
            lifetime (int): Время жизни инвойса в минутах
            amount_currency (str, optional): Валюта суммы. Defaults to None.
            required_method (Union[PAYMENT_METHODS], optional): Заранее заданный метод, плательщик не сможет выбрать другой. Defaults to None.
            payer_details (str, optional): E-mail плательщика. Defaults to None.
            description (str, optional): Описание или назначение. Defaults to None.
            extra (str, optional): Любые данные, например ID платежа в вашей системе. Defaults to None.
            redirect_url (str, optional): Ссылка для перенаправления после оплаты. Defaults to None.
            callback_url (str, optional): Ссылка для отправки http callback уведомления об оплате. Defaults to None.
        """
        data = await self._send_request(
            "POST",
            "invoice/create/",
            {
                "amount": amount,
                "type": type_,
                "lifetime": lifetime,
                "amount_currency": amount_currency,
                "required_method": required_method,
                "payer_details": payer_details,
                "description": description,
                "extra": extra,
                "redirect_url": redirect_url,
                "callback_url": callback_url

            }
        )
        return InvoiceCreate.model_validate(data)
    
    async def invoice_info(self, id_: str) -> InvoiceInfo:
        """Получить информацию о платеже

        Args:
            id_ (str): id платежа
        """
        data = await self._send_request(
            "POST",
            "invoice/info/",
            {
                "id": id_
            }
        )
        return InvoiceInfo.model_validate(data)

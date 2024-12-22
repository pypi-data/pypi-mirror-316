from pycrystalpay.types import MeInfo

from .base import BaseApiWrapper


class Me(BaseApiWrapper):
    """Методы `me` 

    Doc - https://docs.crystalpay.io/metody-api/me-kassa
    """

    async def me_info(self) -> MeInfo:
        """Поулчить информацию о кассе

        Doc - https://docs.crystalpay.io/metody-api/me-kassa/poluchenie-informacii-o-kasse
        """
        data = await self._send_request(
            "POST",
            "me/info/"
        )
        return MeInfo.model_validate(data)

from pydantic import BaseModel


class MeInfo(BaseModel):
    """Ответ метода me/info

    Doc - https://docs.crystalpay.io/metody-api/me-kassa/poluchenie-informacii-o-kasse
    """
    id: int
    name: str
    status_level: int
    created_at: str

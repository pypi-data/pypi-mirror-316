from typing import Dict, Literal, Optional

from pydantic import BaseModel, Field


PAYMENT_METHODS = Literal['BITCOIN', 'BITCOINCASH', 'BNBCRYPTOBOT', 'BNBSMARTCHAIN', 'BTCCRYPTOBOT', 'CARDKZTP2P', 'CARDRUBP2P', 'CRYSTALPAY', 'DASH', 'DOGECOIN', 'ETHCRYPTOBOT', 'ETHEREUM', 'LITECOIN', 'LTCCRYPTOBOT', 'LZTMARKET', 
                          'MONERO', 'POLYGON', 'SBERPAYP2P', 'SBPP2P', 'TEST', 'TONCOIN', 'TONCRYPTOBOT', 'TRON', 'USDCTRC', 'USDTBEP', 'USDTCRYPTOBOT', 'USDTTRC']

class MethodExtraCommissions(BaseModel):
    amount: str
    percent: str

class MethodSettingsInfo(BaseModel):
    enabled: bool
    extra_commissions: MethodExtraCommissions


class MethodSettings(BaseModel):
    in_: MethodSettingsInfo = Field(default_factory=lambda d: d.get("in"))
    out: MethodSettingsInfo

class MethodLimits(BaseModel):
    min: float
    max: float

class MethodComData(BaseModel):
    enabled: bool
    limits: MethodLimits
    fee: str
    commissions: MethodExtraCommissions

class MethodGet(BaseModel):
    """Ответ метода method/get и элемент списка method/list 

    Doc - https://docs.crystalpay.io/metody-api/method-metody/poluchenie-metoda
    """
    name: str
    currency: str
    amount_accuracy: int
    minimal_status_level: int
    settings: MethodSettings
    in_: Optional[MethodComData] = Field(default_factory=lambda d: d.get("in", None))
    out: Optional[MethodComData] = None




class MethodList(BaseModel):
    """Ответ метода method/list

    Doc - https://docs.crystalpay.io/metody-api/method-metody/poluchenie-spiska-metodov
    """
    items: Dict[str, MethodGet]

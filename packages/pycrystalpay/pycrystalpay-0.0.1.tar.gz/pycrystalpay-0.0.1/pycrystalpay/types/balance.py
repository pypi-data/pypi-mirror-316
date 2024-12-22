from typing import Dict, List, Optional, Union

from pydantic import BaseModel


class BalanceGet(BaseModel):
    """Ответ метода balance/get и элемент списка balance/list

    Doc - https://docs.crystalpay.io/metody-api/balance-balansy/poluchenie-balansa
    """
    name: str
    currency: str
    amount_accuracy: int
    amount: str
    method: Optional[str] = None # Optional for balance list



class BalanceList(BaseModel):
    """Ответ метода balance/list

    Doc - https://docs.crystalpay.io/metody-api/balance-balansy/poluchenie-spiska-balansov
    """

    items: Union[Dict[str, BalanceGet], List] # Return empty list if no nozero balances

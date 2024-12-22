from typing import Literal, Optional

from pydantic import BaseModel


SUBSTRUCT_FROM = Literal[
    "balance",
    "amount"
]

class PayoffCreate(BaseModel):
    """Ответ метода payoff/create
    """
    id: str
    subtract_from: str
    method: str
    amount_currency: str
    amount: str
    rub_amount: str
    receive_amount: str
    deduction_amount: str
    commission_amount: str
    wallet: str

class PayoffData(BaseModel):
    """Ответ метода payoff/submit
    """
    id: str
    state: str
    subtract_from: str
    method: str
    amount_currency: str
    amount: str
    rub_amount: str
    receive_amount: Optional[str] = None
    deduction_amount: Optional[str] = None
    commission_amount: Optional[str] = None
    wallet: Optional[str] = None
    message: Optional[str] = None
    callback_url: Optional[str] = None
    extra: Optional[str] = None
    created_at: Optional[str] = None
    final_at: Optional[str] = None
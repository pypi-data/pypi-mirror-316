from typing import Literal, Optional

from pydantic import BaseModel


INVOICE_TYPES = Literal["purchase", "topup"]

INVOICE_STATES = Literal[
    "notpayed",
    "processing",
    "wrongamount",
    "failed",
    "payed",
    "unavailable"
]

class InvoiceCreate(BaseModel):
    """Ответ метода invoice/create
    """    
    id: str
    url: str
    type: str
    rub_amount: str

class InvoiceInfo(BaseModel):
    """Ответ метода invoice/info
    """
    id: str
    url: str
    type: str
    state: str
    method: Optional[str] = None #type: ignore
    required_method: Optional[str] = None #type: ignore
    amount_currency: Optional[str] = None #type: ignore
    rub_amount: Optional[str] = None #type: ignore
    initial_amount: Optional[str] = None #type: ignore
    remaining_amount: Optional[str] = None #type: ignore
    balance_amount: Optional[str] = None #type: ignore
    commission_amount: Optional[str] = None #type: ignore
    description: Optional[str] = None #type: ignore
    redirect_url: Optional[str] = None #type: ignore
    callback_url: Optional[str] = None #type: ignore
    extra: Optional[str] = None #type: ignore
    created_at: Optional[str] = None #type: ignore
    expired_at: Optional[str] = None #type: ignore
    final_at: Optional[str] = None #type: ignore

    @property
    def is_payed(self) -> bool:
        """Оплачен ли платёж
        """
        return self.state == "payed"

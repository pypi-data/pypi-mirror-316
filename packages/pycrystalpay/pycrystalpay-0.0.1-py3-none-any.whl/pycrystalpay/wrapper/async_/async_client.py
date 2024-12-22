from .me import Me
from .balance import Balance
from .method import Method
from .invoice import Invoice
from .payoff import Payoff


class AsyncCrystalPay(Me, Balance, Method, Invoice, Payoff):
    """Асинхронный клиент
    """

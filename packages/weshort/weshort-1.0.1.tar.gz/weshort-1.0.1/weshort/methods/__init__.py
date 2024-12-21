from .payment import Payment
from .shorts import Shorts
from .withdraw import Withdraw

class Methods(
    Payment,
    Shorts,
    Withdraw,
):
    pass

#  Weshort - Shortener URL API Client Library for Python
#  Copyright (C) 2024-present AyiinXd <https://github.com/AyiinXd>
#
#  This file is part of Weshort.
#
#  Weshort is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Weshort is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Weshort.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union

import weshort
from weshort.exception import WeShortError
from weshort.types import CheckedTransaction, Response, TransactionSuccess



class CheckTransaction:
    async def checkTransaction(self: "weshort.WeShort", trxId: str) -> Union[CheckedTransaction, TransactionSuccess]:
        """Check Details Transaction, the main means for interacting with API WeShort.
        
        Parameters:
            trxId (``str``):
                Trx ID is `Transaction ID` or `Order ID` for Getting Details Transaction.
                e.g.: "xxxxx1e2e0c3a062b17025exxxxx75405a5d5a73504f5e26495c0f5a770107".

        Returns:
            ``CheckedTransaction``: CheckedTransaction object.

        Example:
            >>> from weshort import WeShort
            >>> 
            >>> weShort = WeShort(apiToken="YOUR_API_TOKEN")
            >>> try:
            >>>     data = await weShort.checkTransaction("xxxxx1e2e0c3a062b17025exxxxx75405a5d5a73504f5e26495c0f5a770107")
            >>>     print(data) # output: CheckedTransaction object
            >>> except WeShortError as e:
            >>>     print(e)
        """
        res = await self.get(
            f"/payment/check?transactionId={trxId}",
        )
        if not isinstance(res, Response):
            raise WeShortError(res)
        if "data" in res.responseData:
            return TransactionSuccess(**res.responseData)
        return CheckedTransaction(**res.responseData)

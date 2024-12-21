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

from typing import List, Optional

import weshort
from weshort.exception import WeShortError
from weshort.types import Payment, Response


class GetPayment:
    async def getPayments(self: "weshort.WeShort") -> List[Payment]:
        """Get All Payments, the main means for interacting with API WeShort.

        Returns:
            ``List[Payment]``: List of Payment.

        Example:
            >>> from weshort import WeShort
            >>> 
            >>> weShort = WeShort(apiToken="YOUR_API_TOKEN")
            >>> try:
            >>>     url = await weShort.getPayments()
            >>>     print(url) # output: List[Payment]
            >>> except WeShortError as e:
            >>>     print(e)
        """
        res = await self.get(
            f"/payment",
        )
        if not isinstance(res, Response):
            raise WeShortError(res)
        shortsUrl: List[Payment] = [Payment(**x) for x in res.responseData]
        return shortsUrl

    async def getPayment(self: "weshort.WeShort", orderId: str) -> Payment:
        """Get Detail Payment, the main means for interacting with API WeShort.

        Parameters:
            orderId (``str``):
                Order ID for Get Detail Payment.
                e.g.: "xxxxxxxxxx1e2e0c3a062b17025exxxxxxxxxx764b505b5c7053405e351c1a1d5c740e".

        Returns:
            ``Payment``: Payment class.

        Example:
            >>> from weshort import WeShort
            >>> 
            >>> weShort = WeShort(apiToken="YOUR_API_TOKEN")
            >>> try:
            >>>     url = await weShort.getPayment("xxxxxxxxxx1e2e0c3a062b17025exxxxxxxxxx764b505b5c7053405e351c1a1d5c740e")
            >>>     print(url) # output: Payment class
            >>> except WeShortError as e:
                    print(e)
        """
        res = await self.get(
            f"/payment?orderId={orderId}",
        )
        if not isinstance(res, Response):
            raise WeShortError(res)
        return Payment(**res.responseData)

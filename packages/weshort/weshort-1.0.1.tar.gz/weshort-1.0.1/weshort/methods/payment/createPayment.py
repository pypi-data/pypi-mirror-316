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

from typing import List

import weshort
from weshort.exception import WeShortError
from weshort.types import CreatedPayment, Response


class CreatePayment:
    async def createPayment(self: "weshort.WeShort", shortUrl: str) -> CreatedPayment:
        """Create Payments Shortlink, the main means for interacting with API WeShort.
        
        Parameters:
            shortUrl (``str``):
                Short URL for Create Payments.
                e.g.: "https://weshort.pro/xxxxxx".

        Returns:
            ``CreatedPayment``: CreatedPayment object.

        Example:
            >>> from weshort import WeShort
            >>> 
            >>> weShort = WeShort(apiToken="YOUR_API_TOKEN")
            >>> try:
            >>>     data = await weShort.createPayment("https://weshort.pro/tyrqopeb")
            >>>     print(data) # output: CreatedPayment object
            >>> except WeShortError as e:
            >>>     print(e)
        """
        res = await self.post(
            f"/payment?shortUrl={shortUrl}",
        )
        if not isinstance(res, Response):
            raise WeShortError(res)
        return CreatedPayment(**res.responseData)

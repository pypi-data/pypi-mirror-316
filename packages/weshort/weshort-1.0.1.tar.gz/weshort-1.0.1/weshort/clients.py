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

import aiofiles
import aiohttp
import os
from typing import Optional

from .base import Base
from .exception import WeShortError
from .methods import Methods
from .types import GetMe, Response


class WeShort(Base, Methods):
    """WeShort Client, the main means for interacting with API WeShort.

    Parameters:
        apiToken (``str``):
            API token for Authorization Users, e.g.: "AxD_ABCDEFghIklzyxWvuew".
            Get the ``API Token`` in [WeShortProfile](https://weshort.pro).

    Example:
        >>> from weshort import WeShort
        >>> 
        >>> weShort = WeShort(
        >>>     apiToken="YOUR_API_TOKEN"
        >>> )
    """
    def __init__(
        self,
        apiToken: str
    ):
        super().__init__(apiToken=apiToken)

    async def getMe(self) -> GetMe:
        res = await self.get("/client")
        if not isinstance(res, Response):
            raise WeShortError("Failed to get User Info")
        return GetMe(**res.responseData)

    async def deleteAccount(self):
        res = await self.delete("/client")
        if not isinstance(res, Response):
            raise WeShortError("Failed to delete Account")
        return True

    async def generateQris(self, qrisToken: str, uniqueId: Optional[str] = None) -> str:
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
        if not uniqueId:
            # Create Unique Id from qrisToken
            number = "1 2 3 4 5 6 7 8 9 0".split(" ")
            uniqueId = "".join(qrisToken[int(i*3)] for i in number)
        async with aiohttp.ClientSession() as session:
            res = await session.get(
                f"{self.baseUrl}/qris?token={qrisToken}",
                headers=self.headers
            )
            if res.status == 200:
                async with aiofiles.open(f"downloads/WeShortQris-{uniqueId}.png", "wb") as f:
                    async for chunk, _ in res.content.iter_chunks():
                        await f.write(chunk)

        return f"downloads/WeShort-{uniqueId}-Qris.png"

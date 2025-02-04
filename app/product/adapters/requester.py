import abc
import asyncio

import aiohttp

from app.product.exceptions import HttpProductRequesterError
from app.settings import CHALLENGE_API


class ProductRequester(abc.ABC):
    def __init__(self):
        self.api_url = CHALLENGE_API
        self.get_timeout = 5

    @abc.abstractmethod
    async def get(
        self,
        product_id: str,
    ): ...  # pragma: nocoverage


class ProductAiohttpRequester(ProductRequester):
    def __init__(self, session: aiohttp.ClientSession):
        super().__init__()
        self.session = session

    async def get(self, product_id: str):
        url = f"{self.api_url}/product/{product_id}/"
        try:
            async with self.session.get(
                url, timeout=aiohttp.ClientTimeout(total=self.get_timeout)
            ) as response:
                response.raise_for_status()
                return await response.json()
        except aiohttp.ClientResponseError as e:
            HttpProductRequesterError(str(e))
        except aiohttp.ClientError as e:
            HttpProductRequesterError(str(e))
        except asyncio.TimeoutError:
            HttpProductRequesterError(f"Timeout error for url {url}")

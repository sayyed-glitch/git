from typing import Optional

import aiohttp
from loguru import logger
from requests import RequestException

from reworkd_platform.schemas.workflow.base import Block, BlockIOBase


class UrlStatusCheckBlockInput(BlockIOBase):
    url: str


class UrlStatusCheckBlockOutput(BlockIOBase):
    code: Optional[int]


class UrlStatusCheckBlock(Block):
    type = "UrlStatusCheck"
    description = "Outputs the status code of a GET request to a URL"
    image_url = ""
    input: UrlStatusCheckBlockInput

    async def run(self) -> BlockIOBase:
        logger.info(f"Starting UrlStatusCheckBlock with url: {self.input.url}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.input.url) as response:
                    code = response.status
        except RequestException:
            pass
        finally:
            logger.info(f"UrlStatusCheckBlock Response: {response}")

        logger.info(f"UrlStatusCheckBlock Code: {code}")
        output = UrlStatusCheckBlockOutput(code=code)
        return output

import requests
import asyncio
import aiohttp as aiohttp
from aiohttp import ClientTimeout
from pyppeteer import launch


class GrabberMixin:
    def __init__(self, timeout=60):
        self.timeout = timeout

    async def grab(self, url: str) -> str:
        """Grab html from url."""
        raise NotImplemented()


class RequestsGrabber(GrabberMixin):
    """Synchronous implementation using the library requests."""
    async def grab(self, url: str) -> str:
        return requests.get(url).text


class AiohttpGrabber(GrabberMixin):
    async def grab(self, url: str) -> str:
        async with aiohttp.ClientSession(
                timeout=ClientTimeout(total=self.timeout),
                headers={"Accept": "text/html"}
        ) as session:
            async with session.get(url) as resp:
                return await resp.text()


class PyppeteerGrabber(GrabberMixin):
    async def grab(self, url: str) -> str:
        browser = await launch()
        page = await browser.newPage()
        await page.goto(url, timeout=self.timeout)
        content = await page.content()
        await browser.close()
        return content

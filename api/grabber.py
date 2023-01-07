import aiohttp as aiohttp
import requests
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
        try:
            async with aiohttp.ClientSession(
                    timeout=ClientTimeout(total=self.timeout),
                    headers={"Accept": "text/html"}
            ) as session:
                async with session.get(url) as resp:
                    return await resp.text()
        except:
            # log error
            return ""


class PyppeteerGrabber(GrabberMixin):
    def __init__(self, timeout: int = 300*1000):
        super().__init__(timeout)
        self._browser = None

    async def init_browser(self):
        self._browser = await launch(
            headless=True,
            executablePath="/usr/bin/chromium-browser",
            handleSIGINT=False,
            handleSIGTERM=False,
            handleSIGHUP=False,
            args=[
                '--no-sandbox',
                '--single-process',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--no-zygote'
            ]
        )

    async def grab(self, url: str) -> str:
        page = await self._browser.newPage()
        await page.goto(url, timeout=self.timeout)
        content = await page.content()
        await page.close()
        return content

    async def close_browser(self) -> None:
        await self._browser.close()


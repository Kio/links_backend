import asyncio
import urllib.parse
from typing import Set, List
from bs4 import BeautifulSoup

from api.grabber import GrabberMixin, PyppeteerGrabber, AiohttpGrabber

MAX_DEPTH = 2


def __absolute_href(base_url: str, url: str) -> str:
    """Construct absolute url from base and relative url."""
    return urllib.parse.urljoin(base_url, url)


def __filter_url(url: str) -> bool:
    """Filter links to other pages."""
    url = url.lower()
    return not url.startswith((
            "#",
            "javascript:",
            "news:",
            "mailto:",
            "irc:",
        )) and not url.endswith(tuple(map(lambda ext: f".{ext}", [
            "jpg",
            "png",
            "pdf",
            "jpeg",
            "doc",
            "txt",
            "json",
            "xml",
            "docx"
        ])))


def __find_links_in_html(html: str) -> list[str]:
    """Find all links and return them as list."""
    soup = BeautifulSoup(html, "lxml")
    links = soup.find_all('a', href=True)
    links = map(lambda link: link.get("href"), links)
    return list(links)


async def __links_list_from_url(url: str, grabbers: List[GrabberMixin]) -> List[str]:
    """Use list of grabbers to get html and then extract list of links."""
    other_pages_links = []
    for grabber in grabbers:
        try:
            html = await grabber.grab(url)
        except Exception as error:
            # Log error for future analyse
            continue
        html_links = __find_links_in_html(html)
        absolute_links = map(lambda link_: __absolute_href(url, link_), html_links)
        other_pages_links = list(filter(__filter_url, absolute_links))
        if len(other_pages_links) > 0:  # try another grabber only if no links to other pages
            break
    return other_pages_links


async def __extract_links_to_set_with_grabbers(
    url: str,
    links: Set[str],
    grabbers: List[GrabberMixin],
    depth: int = 0,
) -> None:
    """Add all links to given set and call recursive for nested links if depth < MAX_DEPTH."""
    nested_links = await __links_list_from_url(url, grabbers)
    tasks = []
    for link in nested_links:
        links.add(link)
        if depth + 1 < MAX_DEPTH:
            tasks.append(
                asyncio.ensure_future(
                    __extract_links_to_set_with_grabbers(link, links, grabbers, depth + 1)
                )
            )
    try:
        await asyncio.gather(*tasks)
    except Exception as error:
        # Log error for future analyse
        pass


async def extract_links_to_set(
    url: str,
    links: Set[str]
) -> None:
    pg = PyppeteerGrabber()
    await pg.init_browser()
    await __extract_links_to_set_with_grabbers(
        url,
        links,
        [AiohttpGrabber(), pg]
    )
    await pg.close_browser()

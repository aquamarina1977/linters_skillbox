import asyncio
import aiohttp
import aiofiles
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

DEFAULT_DEPTH = 3
OUTPUT_FILE = "external_links.txt"

async def fetch(session, url):
    try:
        async with session.get(url) as res:
            return await res.text()
    except Exception as e:
        print(e)
        return None

async def extract_external_links(session, url, base_domain):
    html = await fetch(session, url)
    if not html:
        return set()
    soup = BeautifulSoup(html, 'html.parser')
    links = set()
    for link in soup.find_all('a', href=True):
        full_url = urljoin(url, link['href'])
        parsed_url = urlparse(full_url)
        if parsed_url.netloc and parsed_url.netloc != base_domain:
            links.add(full_url)
    return links

async def crawl(start_urls, depth=DEFAULT_DEPTH):
    visited = set()
    external_links = set()
    async with aiohttp.ClientSession() as session:
        for _ in range(depth):
            tasks = []
            for url in start_urls - visited:
                visited.add(url)
                base_domain = urlparse(url).netloc
                tasks.append(extract_external_links(session, url, base_domain))
                new_links = await asyncio.gather(*tasks)
                for links in new_links:
                    external_links.update(links)
                start_urls = external_links - links
    await save_links(external_links)

async def save_links(links):
    async with aiofiles.open(OUTPUT_FILE, 'w') as f:
        await f.write("\n".join(links))

if __name__ == "__main__":
    start_urls = {"https://habr.com/ru/feed/"}
    asyncio.run(crawl(start_urls))

import asyncio
from pathlib import Path
import aiohttp
import time

URL = 'https://cataas.com/cat'
CATS_WE_WANT = 10
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()

async def get_cat(client: aiohttp.ClientSession, idx: int) -> bytes:
    async with client.get(URL) as response:
        print(response.status)
        result = await response.read()
        await write_to_disk(result, idx)

async def write_to_disk(content: bytes, id: int):
    file_path = OUT_PATH / f"{id}.png"
    await asyncio.to_thread(write_file, file_path, content)

def write_file(file_path: Path, content: bytes):
    with open(file_path, mode="wb") as f:
        f.write(content)

async def get_all_cats():
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as client:
        tasks = [get_cat(client, i) for i in range(CATS_WE_WANT)]
        return await asyncio.gather(*tasks)

def main():
    start = time.perf_counter()
    res = asyncio.run(get_all_cats())
    print(time.perf_counter() - start)
    print(len(res))

if __name__ == '__main__':
    main()

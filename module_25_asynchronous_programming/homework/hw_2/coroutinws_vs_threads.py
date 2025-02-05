import asyncio
import time
import psutil
from pathlib import Path
import aiohttp
import aiofiles
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import requests

from module_25_asynchronous_programming.homework.hw_1.async_app import OUT_PATH, write_to_disk

URL = 'https://cataas.com/cat'
OUT_PATH = Path(__file__).parent / 'cats'
OUT_PATH.mkdir(exist_ok=True, parents=True)
OUT_PATH = OUT_PATH.absolute()

#Корутины
async def get_cat_async(client: aiohttp.ClientSession, idx: int):
    async with client.get(URL) as response:
        content = await response.read()
        await write_to_disk(content, idx)

async def write_to_disk(content: bytes, idx: int):
    file_path = OUT_PATH / f"{idx}.png"
    async with aiofiles.open(file_path, mode='wb') as f:
        await f.write(content)

async def download_cats_async(n):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(15)) as client:
        tasks = [get_cat_async(client, i) for i in range(n)]
        await asyncio.gather(*tasks)

#Потоки
def get_cat_threaded(idx):
    response = requests.get(URL)
    if response.status_code == 200:
        write_cont_to_disk(response.content, idx)

def write_cont_to_disk(content: bytes, idx: int):
    file_path = OUT_PATH / f"{idx}.png"
    with open(file_path, 'wb') as f:
        f.write(content)

def download_cats_threaded(n):
    with ThreadPoolExecutor() as ex:
        ex.map(get_cat_threaded, range(n))

#Процессы
def get_cat_processed(idx):
    response = requests.get(URL)
    if response.status_code == 200:
        write_cont_to_disk(response.content, idx)

def download_cats_processed(n):
    with ProcessPoolExecutor() as ex:
        ex.map(get_cat_processed, range(n))

#Проверка CPU
def benchmark(func, n):
    start_time = time.perf_counter()
    cpu_before = psutil.cpu_percent()
    mem_before = psutil.virtual_memory().percent
    func(n)
    cpu_after = psutil.cpu_percent()
    mem_after = psutil.virtual_memory().percent
    end_time = time.perf_counter()
    return end_time - start_time, cpu_after - cpu_before, mem_after - mem_before

def benchmark_async(n):
    start_time = time.perf_counter()
    cpu_before = psutil.cpu_percent()
    mem_before = psutil.virtual_memory().percent
    asyncio.run(download_cats_async(n))
    cpu_after = psutil.cpu_percent()
    mem_after = psutil.virtual_memory().percent
    end_time = time.perf_counter()
    return end_time - start_time, cpu_after - cpu_before, mem_after - mem_before

if __name__ == "__main__":
    for count in [10, 50, 100]:
        async_time, async_cpu, async_mem = benchmark_async(count)
        thread_time, thread_cpu, thread_mem = benchmark(download_cats_threaded, count)
        process_time, process_cpu, process_mem = benchmark(download_cats_processed, count)
        print("-" * 50)
        print(f"|Корутины: {async_time:.2f} сек| CPU: {async_cpu:.2f}%| RAM: {async_mem:.2f}%|")
        print("-" * 50)
        print(f"|Потоки:   {thread_time:.2f} сек| CPU: {thread_cpu:.2f}% | RAM: {thread_mem:.2f}% |")
        print("-" * 50)
        print(f"|Процессы: {process_time:.2f} сек| CPU: {process_cpu:.2f}% | RAM: {process_mem:.2f}% |")
        print("-" * 50)
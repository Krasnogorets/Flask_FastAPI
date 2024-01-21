"""
Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. Каждое изображение
должно сохраняться в отдельном файле, название которого соответствует названию изображения в URL-адресе.
Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
— Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
— Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
— Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем времени выполнения программы.
"""
import threading
from multiprocessing import Process
import time
import asyncio
import aiohttp
import requests


urls = ['https://cloud.yatco.com/ForSale/Vessel/Photo/379295/large_3911755.png',
        'https://cloud.yatco.com/ForSale/Vessel/Photo/379295/large_3911757.png',
        'https://cloud.yatco.com/ForSale/Vessel/Photo/379295/large_3911758.png',
        'https://cloud.yatco.com/ForSale/Vessel/Photo/379295/large_3911759.png',
        'https://cloud.yatco.com/ForSale/Vessel/Photo/379295/large_3911760.png',
        'https://cloud.yatco.com/ForSale/Vessel/Photo/379295/large_3911761.png',
        "https://cloud.yatco.com/ForSale/Vessel/Photo/379295/large_3911762.png",
        "https://cloud.yatco.com/ForSale/Vessel/Photo/379295/large_3911763.png"]


def download(url, path_):
    start_time = time.time()
    response = requests.get(url)
    filename = path_ + url.replace('https://cloud.yatco.com/ForSale/Vessel/Photo/379295/', '').replace('/', '')
    with open(filename, "wb") as f:
        f.write(response.content)
        print(f"Downloaded {url} in {time.time() - start_time:.5f}seconds")


def threading_():
    threads = []
    path_ = 'threading/'
    start_time = time.time()
    for url in urls:
        thread = threading.Thread(target=download, args=[url, path_])
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    print(f"all threading process in {time.time() - start_time:.2f}seconds")


def processing():
    processes = []
    path_ = 'processing/'
    start_time = time.time()
    for url in urls:
        process = Process(target=download, args=(url, path_,))
        processes.append(process)
        process.start()
    for process in processes:
        process.join()
    print(f"all multiprocessing  in {time.time() - start_time:.2f}seconds")


async def download_as(url):
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            img = await response.content.read()
            filename = 'asyncio/' + url.replace('https://cloud.yatco.com/ForSale/Vessel/Photo/379295/', '') \
                .replace('/', '')
            with open(filename, "wb") as f:
                f.write(img)
            print(f"Downloaded {url} in {time.time() - start_time:.2f} seconds")


async def as_start():
    start_time = time.time()
    tasks = []
    for url in urls:
        task = asyncio.ensure_future(download_as(url))
        tasks.append(task)
    await asyncio.gather(*tasks)
    print(f"all asyncio process in {time.time() - start_time:.2f}seconds")


if __name__ == '__main__':
    threading_()
    processing()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(as_start())

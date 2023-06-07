"""
Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск. Каждое изображение
должно сохраняться в отдельном файле, название которого соответствует названию изображения в URL-адресе.
Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
— Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
— Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
— Программа должна выводить в консоль информацию о времени скачивания каждого изображения и общем времени выполнения
программы.
"""

import time
import threading
import multiprocessing
import asyncio
import aiohttp
import requests
import os
from urllib.parse import urlparse
import sys

IMG_URLS = [
    'https://tengrinews.kz/userdata/1(279).jpg',
    'https://kartinki.pibig.info/uploads/posts/2023-04/thumbs/1682259422_kartinki-pibig-info-p-kartinka-samaya-bolshaya-arti-krasivo-1.jpg',
    'https://thebiggest.ru/wp-content/uploads/2018/12/kartiny-870x400.jpg',
    'https://cameralabs.org/media/k2/items/cache/5e3bd17765e820213981ad5d80fbce34_L.jpg'
]


def get_filename(img_url):
    a = urlparse(img_url)
    return os.path.basename(a.path)


def img_download(img_url):
    _time = time.time()
    image = requests.get(img_url).content
    file_name = get_filename(img_url)
    with open(file_name, 'wb') as handler:
        handler.write(image)
    print(f'{img_url} - {(time.time() - _time)}')


async def img_download_async(img_url):
    _time = time.time()
    async with aiohttp.ClientSession() as session:
        async with session.get(img_url) as response:
            file_name = get_filename(img_url)
            with open(file_name, 'wb') as handler:
                image = await response.read()
                handler.write(image)
                print(f'{img_url} - {(time.time() - _time)}')


if __name__ == '__main__':
    start_full_time = time.time()

    urls = IMG_URLS

    if len(sys.argv) > 1:
        urls = sys.argv[1:]

    # Многопоточность
    start_time = time.time()
    threads = []
    for url in urls:
        t = threading.Thread(target=img_download, args=(url,))
        threads.append(t)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(f'Threads Ready! - {(time.time() - start_time)}')

    # Многопроцессорность
    start_time = time.time()
    processes = []
    for url in urls:
        p = multiprocessing.Process(target=img_download, args=(url,))
        processes.append(p)

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    print(f'Processes Ready! - {(time.time() - start_time)}')

    # Асинхронность
    start_time = time.time()
    async_tasks = []
    for url in urls:
        task = asyncio.ensure_future(img_download_async(url,))
        async_tasks.append(task)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(async_tasks))

    print(f'Asyncio Ready! - {(time.time() - start_time)}')

    print(f'Общее время - {(time.time() - start_full_time)}')

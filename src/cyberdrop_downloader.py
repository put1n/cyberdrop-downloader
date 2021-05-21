import os
import re
import lxml
import requests
import asyncio
import aiohttp

from progress_bar import *

from bs4 import BeautifulSoup
from dataclasses import dataclass, field


class CyberDropDownloader:
    @dataclass
    class File:
        name: str
        url: str

    @dataclass
    class Album:
        url: str = None
        name: str = None
        dir: str = None
        length: int = None
        files: list = field(default_factory=lambda: [])

    def __init__(self, album_id, root_path_to_save=os.getcwd()):
        self.__album = self.Album()
        self.__album.url = 'https://cyberdrop.me/a/' + album_id

        self.__root_path_to_save = root_path_to_save

        self.__progress_bar = ProgressBar(0)

    async def run(self):
        self.__scrape_album()

        self.__progress_bar.show_progress()

        tasks = []

        for file in self.__album.files:
            task = asyncio.create_task(self.__download_and_save_task(file.url, file.name))
            tasks.append(task)

        await asyncio.wait(tasks)

    def __scrape_album(self):
        with requests.Session() as session:
            headers = {
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 '
                              'Safari/537.36',
            }

            content = session.get(self.__album.url, headers=headers).content

        soup = BeautifulSoup(content, 'lxml')

        file_links = soup.findAll('a', {'class': 'image'})
        urls = [file_link['href'] for file_link in file_links]

        if not urls:
            return None

        for file_link in file_links:
            name = file_link['title']
            url = file_link['href']

            file = self.File(name, url)
            self.__album.files.append(file)

        self.__progress_bar.set_actions_to_do(len(self.__album.files) * 2)

        self.__album.name = self.__clean_text(soup.find('h1', {'id': 'title'})['title'])
        self.__album.dir = os.path.join(self.__root_path_to_save, self.__album.name)
        self.__album.length = len(urls)

        os.makedirs(self.__album.dir, exist_ok=True)

    @staticmethod
    def __clean_text(string):
        pattern = re.compile(r'[\\/:*?"<>|]')
        clean_string = pattern.sub('_', string)

        return clean_string

    async def __download_file(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                content = await resp.read()
                self.__progress_bar.show_progress()

                return content

    async def __write_to_file(self, filename, content):
        path = os.path.join(self.__album.dir, filename)

        if os.path.isfile(path):
            return

        with open(path, "wb+") as file:
            file.write(content)

        self.__progress_bar.show_progress()

    async def __download_and_save_task(self, url, filename):
        content = await self.__download_file(url)
        await self.__write_to_file(filename, content)

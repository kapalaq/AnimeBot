import requests
from bs4 import BeautifulSoup

import re
import os

from sign_dict import ChangeSigns
from database import Database
from youtube_download import Download


class Functions:

    @staticmethod
    def find(value):
        url = f'https://myanimelist.net/anime.php?q={ChangeSigns.change_signs(str(value))}&cat=anime'
        answer = Parsing(url)
        mass = []
        db = Database()
        db.name = "anime_search"
        for i, content in enumerate(answer.get_search()):
            db.insert((i, content.get('href')))
            mass.append((content.text, i))
        return mass

    @staticmethod
    async def trailer(value):
        return await Parsing(value).get_trailer()

    @staticmethod
    async def poster(value):
        return await Parsing(value).get_poster()


class Parsing:

    def __init__(self, url):
        self.response = requests.get(url)
        self.soup = BeautifulSoup(self.response.text, 'lxml')

    def get_search(self):
        try:
            titles = self.soup.find_all('a', class_='hoverinfo_trigger')
            titles = list(filter(lambda x: 'img' not in str(x), titles))
        except Exception as error:
            print("Search error:", error)
            titles = None
        return titles

    async def get_poster(self):
        try:
            title = self.soup.find_all('h1', class_='title-name h1_bold_none')[0].text
            poster = self.soup.find('img', alt=title).get('data-src')
        except Exception as error:
            print("Poster error:", error)
            url = None
        else:
            url = await self.download(poster, title, '.jpg')
        return url

    async def get_trailer(self):
        try:
            yt = self.soup.find('a', class_='iframe js-fancybox-video video-unit promotion').get('href')
        except Exception as error:
            print("Trailer error:", error)
            url = None
        else:
            video = Download('media/', yt)
            url = await video.download_video()
        return url

    async def download(self, url, title, typeOf):
        if not os.path.exists(f'media/{title}{typeOf}'):
            img = requests.get(url)
            with open(f'media/{title}{typeOf}', 'wb') as out:
                out.write(img.content)
        return f'media/{title}{typeOf}'

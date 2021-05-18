import aiohttp
from bs4 import BeautifulSoup
from pathlib import Path
import re
from datetime import datetime

try:
    import ujson as json
except ModuleNotFoundError:
    import json

headers = {'User-Agent': '"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"'}

# up_char_file = Path() / "data" / "draw_card" / "draw_card_up" / "prts_up_char.json"


class PrtsAnnouncement:
    def __init__(self):
        self.url = "https://wiki.biligame.com/arknights/%E6%96%B0%E9%97%BB%E5%85%AC%E5%91%8A"
        # up_char_file.parent.mkdir(parents=True, exist_ok=True)

    async def get_announcement_text(self):
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(self.url, timeout=7) as res:
                soup = BeautifulSoup(await res.text(), 'lxml')
                trs = soup.find('table').find('tbody').find_all('tr')
                for tr in trs:
                    a = tr.find_all('td')[-1].find('a')
                    if a.text.find('寻访') != -1:
                        url = a.get('href')
                        break
            async with session.get(f'https://wiki.biligame.com/{url}', timeout=7) as res:
                return await res.text(), a.text[:-4]

    def _get_up_char(self, r: str, text: str):
        pr = re.search(r, text)
        chars = pr.group(1)
        probability = pr.group(2)
        chars = chars.replace('[限定]', '').replace('[', '').replace(']', '')
        probability = probability.replace('【', '')
        return chars, probability

    async def update_up_char(self):
        data = {'up_char': {'6': {}, '5': {}, '4': {}}, 'title': '', 'time': ''}
        text, title = await self.get_announcement_text()
        soup = BeautifulSoup(text, 'lxml')
        data['title'] = title
        context = soup.find('div', {'id': 'mw-content-text'}).find('div')
        data['pool_img'] = str(context.find('div', {'class': 'center'}).find('div').find('a').
                               find('img').get('srcset')).split(' ')[-2]
        # print(context.find_all('p'))
        for p in context.find_all('p')[1:]:
            if p.text.find('活动时间') != -1:
                pr = re.search(r'.*?活动时间：(.*)', p.text)
                data['time'] = pr.group(1)
            elif p.text.find('★★★★★★') != -1:
                chars, probability = self._get_up_char(r'.*?★★★★★★：(.*?)（.*?出率的?(.*?)%.*?）.*?', p.text)
                for char in chars.split('\\'):
                    data['up_char']['6'][char.strip()] = probability.strip()
            elif p.text.find('★★★★★') != -1:
                chars, probability = self._get_up_char(r'.*?★★★★★：(.*?)（.*?出率的?(.*?)%.*?）.*?', p.text)
                for char in chars.split('\\'):
                    data['up_char']['5'][char.strip()] = probability.strip()
            elif p.text.find('★★★★') != -1:
                chars, probability = self._get_up_char(r'.*?★★★★：(.*?)（.*?出率的?(.*?)%.*?）.*?', p.text)
                for char in chars.split('\\'):
                    data['up_char']['4'][char.strip()] = probability.strip()
                break
            pr = re.search(r'.*?★：(.*?)（在(.*?)★.*?以(.*?)倍权值.*?）.*?', p.text)
            if pr:
                char = pr.group(1)
                star = pr.group(2)
                weight = pr.group(3)
                char = char.replace('[限定]', '').replace('[', '').replace(']', '')
                data['up_char'][star][char.strip()] = f'权{weight}'
        # data['time'] = '03月09日16:00 - 05月23日03:59'
        if is_expired(data):
            data['title'] = ''
        return data


# async def check_up_char(game_name: str):
#     if game_name == 'prts':
#         text, title = await PrtsAnnouncement().get_announcement_text()
#         if title == data['title']:
#             if is_expired(data):
#                 print('当前up池已结束')
#                 data['title'] = ''
#         else:
#             await PrtsAnnouncement().update_up_char()


def is_expired(data: dict):
    end_date = datetime.strptime(
        str(datetime.now().year) + "-"
        + data['time'].split('-')[-1].split('日')[-2].
        replace('月', '-').replace('日', '').strip(), '%Y-%m-%d').date()
    now = datetime.now().date()
    return now > end_date


# ad = Announcement('https://wiki.biligame.com/arknights/%E6%96%B0%E9%97%BB%E5%85%AC%E5%91%8A')
# asyncio.get_event_loop().run_until_complete(check_up_char('prts'))

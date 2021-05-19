import ujson as json
import os
import nonebot
from nonebot.adapters.cqhttp import MessageSegment
from .update_game_info import update_info
from .util import download_img, init_star_rst, generate_img, max_card
import random
from .config import PRETTY_THREE, PRETTY_TWO, DRAW_PATH

driver: nonebot.Driver = nonebot.get_driver()

pretty_char_dict = {}
pretty_card_dict = {}
THREE_LIST = []
SSR_LIST = []
TWO_LIST = []
SR_LIST = []
ONE_LIST = []
R_LIST = []


async def pretty_draw(count: int, pool_name):
    if pool_name == 'card':
        cnlist = ['SSR', 'SR', 'R']
        A_LIST = SSR_LIST
        B_LIST = SR_LIST
        C_LIST = R_LIST
    else:
        cnlist = ['★★★', '★★', '★']
        A_LIST = THREE_LIST
        B_LIST = TWO_LIST
        C_LIST = ONE_LIST
    obj_list, obj_dict, three_list, star_list, three_olist = _format_card_information(count, pool_name)
    rst = init_star_rst(star_list, cnlist, three_list, three_olist)
    if count > 100:
        obj_list = set(obj_list)
    return MessageSegment.image("base64://" + await generate_img(obj_list, 'pretty', star_list, [A_LIST, B_LIST, C_LIST])) \
           + '\n' + rst[:-1] + '\n' + max_card(obj_dict)


async def update_pretty_info():
    global pretty_char_dict, pretty_card_dict, TWO_LIST, THREE_LIST, ONE_LIST, SSR_LIST, SR_LIST, R_LIST
    url = 'https://wiki.biligame.com/umamusume/赛马娘图鉴'
    data, code = await update_info(url, 'pretty')
    if code == 200:
        pretty_char_dict = data
        THREE_LIST = [pretty_char_dict[char]['名称'] for char in pretty_char_dict.keys() if
                      pretty_char_dict[char]['初始星级'] == 3]
        TWO_LIST = [pretty_char_dict[char]['名称'] for char in pretty_char_dict.keys() if
                    pretty_char_dict[char]['初始星级'] == 2]
        ONE_LIST = [pretty_char_dict[char]['名称'] for char in pretty_char_dict.keys() if
                    pretty_char_dict[char]['初始星级'] == 1]
    url = 'https://wiki.biligame.com/umamusume/支援卡图鉴'
    data, code = await update_info(url, 'pretty_card')
    if code == 200:
        pretty_card_dict = data
        SSR_LIST = [pretty_card_dict[card]['中文名'] for card in pretty_card_dict.keys() if
                    pretty_card_dict[card]['稀有度'] == "SSR"]
        SR_LIST = [pretty_card_dict[card]['中文名'] for card in pretty_card_dict.keys() if
                   pretty_card_dict[card]['稀有度'] == "SR"]
        R_LIST = [pretty_card_dict[card]['中文名'] for card in pretty_card_dict.keys() if
                  pretty_card_dict[card]['稀有度'] == "R"]


@driver.on_startup
async def init_data():
    global pretty_char_dict, pretty_card_dict, TWO_LIST, THREE_LIST, ONE_LIST, SSR_LIST, SR_LIST, R_LIST
    if not os.path.exists(DRAW_PATH + 'pretty.json') or not os.path.exists(DRAW_PATH + 'pretty_card.json'):
        await update_pretty_info()
    else:
        with open(DRAW_PATH + 'pretty.json', 'r', encoding='utf8') as f:
            pretty_char_dict = json.load(f)
        with open(DRAW_PATH + 'pretty_card.json', 'r', encoding='utf8') as f:
            pretty_card_dict = json.load(f)
        THREE_LIST = [pretty_char_dict[char]['名称'] for char in pretty_char_dict.keys() if
                      pretty_char_dict[char]['初始星级'] == 3]
        TWO_LIST = [pretty_char_dict[char]['名称'] for char in pretty_char_dict.keys() if
                    pretty_char_dict[char]['初始星级'] == 2]
        ONE_LIST = [pretty_char_dict[char]['名称'] for char in pretty_char_dict.keys() if
                    pretty_char_dict[char]['初始星级'] == 1]
        SSR_LIST = [pretty_card_dict[card]['中文名'] for card in pretty_card_dict.keys() if
                    pretty_card_dict[card]['稀有度'] == "SSR"]
        SR_LIST = [pretty_card_dict[card]['中文名'] for card in pretty_card_dict.keys() if
                   pretty_card_dict[card]['稀有度'] == "SR"]
        R_LIST = [pretty_card_dict[card]['中文名'] for card in pretty_card_dict.keys() if
                  pretty_card_dict[card]['稀有度'] == "R"]
    for icon_url in [
        'https://patchwiki.biligame.com/images/umamusume/thumb/0/06/q23szwkbtd7pfkqrk3wcjlxxt9z595o.png'
        '/40px-SSR.png',
        'https://patchwiki.biligame.com/images/umamusume/thumb/3/3b/d1jmpwrsk4irkes1gdvoos4ic6rmuht.png'
        '/40px-SR.png',
        'https://patchwiki.biligame.com/images/umamusume/thumb/f/f7/afqs7h4snmvovsrlifq5ib8vlpu2wvk.png'
        '/40px-R.png']:
        await download_img(icon_url, 'pretty', icon_url.split('-')[-1][:-4])


# 抽取卡池
def _get_pretty_card(itype):
    rand = random.random()
    # 普通抽
    if rand < PRETTY_THREE:
        if itype == 'card':
            return random.choice(SSR_LIST), 0
        return random.choice(THREE_LIST), 0
    elif rand < PRETTY_TWO:
        if itype == 'card':
            return random.choice(SR_LIST), 1
        return random.choice(TWO_LIST), 1
    else:
        if itype == 'card':
            return random.choice(R_LIST), 2
        return random.choice(ONE_LIST), 2


# 整理数据
def _format_card_information(count: int, pool_name: str):
    three_list = []
    three_olist = []
    obj_list = []
    obj_dict = {}
    star_list = [0, 0, 0]
    for i in range(count):
        name, code = _get_pretty_card(pool_name)
        star_list[code] += 1
        if code == 0:
            three_list.append(name)
            three_olist.append(i)
        try:
            obj_dict[name] += 1
        except KeyError:
            obj_dict[name] = 1
        obj_list.append(name)
    return obj_list, obj_dict, three_list, star_list, three_olist











import ujson as json
import os
from nonebot.adapters.cqhttp import MessageSegment
import nonebot
import random
from .update_game_info import update_info
from .util import generate_img, init_star_rst, BaseData, set_list, get_star, max_card
from .config import PRC_TWO_P, PRC_THREE_P, PRC_ONE_P, DRAW_PATH, PRC_FLAG, PRC_G_TWO_P, PRC_G_THREE_P
from dataclasses import dataclass
from .init_card_pool import init_game_pool

driver: nonebot.Driver = nonebot.get_driver()

ALL_CHAR = []


@dataclass
class PrcChar(BaseData):
    pass


async def prc_draw(count: int):
    #            0      1      2
    cnlist = ['★★★', '★★', '★']
    char_list, three_list, three_index_list, char_dict, star_list = _format_card_information(count)
    rst = init_star_rst(star_list, cnlist, three_list, three_index_list)
    if count > 90:
        char_list = set_list(char_list)
    return MessageSegment.image("base64://" + await generate_img(char_list, 'prc', star_list)) \
           + '\n' + rst[:-1] + '\n' + max_card(char_dict)


async def update_prc_info():
    global ALL_CHAR
    url = 'https://wiki.biligame.com/pcr/角色筛选表'
    data, code = await update_info(url, 'prc')
    if code == 200:
        ALL_CHAR = init_game_pool('prc', data, PrcChar)


@driver.on_startup
async def init_data():
    global ALL_CHAR
    if PRC_FLAG:
        if not os.path.exists(DRAW_PATH + 'prc.json'):
            await update_prc_info()
        else:
            with open(DRAW_PATH + 'prc.json', 'r', encoding='utf8') as f:
                prc_dict = json.load(f)
            ALL_CHAR = init_game_pool('prc', prc_dict, PrcChar)


# 抽取卡池
def _get_prc_card(mode: int = 1):
    global ALL_CHAR
    if mode == 2:
        star = get_star([3, 2], [PRC_G_THREE_P, PRC_G_TWO_P])
    else:
        star = get_star([3, 2, 1], [PRC_THREE_P, PRC_TWO_P, PRC_ONE_P])
    chars = [x for x in ALL_CHAR if x.star == star and not x.limited]
    return random.choice(chars), abs(star - 3)


def _format_card_information(_count: int):
    char_list = []
    star_list = [0, 0, 0]
    three_index_list = []
    three_list = []
    char_dict = {}
    # 保底计算
    count = 0
    for i in range(_count):
        count += 1
        # 十连保底
        if count == 10:
            char, code = _get_prc_card(2)
            count = 0
        else:
            char, code = _get_prc_card()
            if code == 1:
                count = 0
        star_list[code] += 1
        if code == 0:
            three_list.append(char.name)
            three_index_list.append(i)
        try:
            char_dict[char.name] += 1
        except KeyError:
            char_dict[char.name] = 1
        char_list.append(char)
    return char_list, three_list, three_index_list, char_dict, star_list

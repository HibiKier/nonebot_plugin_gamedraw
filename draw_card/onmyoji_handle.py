
from nonebot.adapters.cqhttp import MessageSegment
import random
from .update_game_requests_info import update_requests_info
from .util import generate_img, init_star_rst, BaseData, set_list, get_star, max_card, format_card_information
from .config import ONMYOJI_SR, ONMYOJI_SSR, ONMYOJI_SP, ONMYOJI_R, DRAW_PATH, ONMYOJI_FLAG
from dataclasses import dataclass
from .init_card_pool import init_game_pool
import nonebot
try:
    import ujson as json
except ModuleNotFoundError:
    import json

ALL_CHAR = []


@dataclass
class OnmyojiChar(BaseData):
    pass


async def onmyoji_draw(count: int):
    #            0      1      2
    cnlist = ['SP', 'SSR', 'SR', 'R']
    star_list = [0, 0, 0, 0]
    char_list, char_dict, max_star_list, star_list, max_star_index_list = \
        format_card_information(count, star_list, _get_onmyoji_card)
    rst = init_star_rst(star_list, cnlist, max_star_list, max_star_index_list)
    if count > 90:
        char_list = set_list(char_list)
    return MessageSegment.image("base64://" + await generate_img(char_list, 'onmyoji', star_list)) \
           + '\n' + rst[:-1] + '\n' + max_card(char_dict)


async def update_onmyoji_info():
    global ALL_CHAR
    data, code = await update_requests_info('onmyoji')
    if code == 200:
        ALL_CHAR = init_game_pool('onmyoji', data, OnmyojiChar)


async def init_onmyoji_data():
    global ALL_CHAR
    if ONMYOJI_FLAG:
        with open(DRAW_PATH + 'onmyoji.json', 'r', encoding='utf8') as f:
            azur_dict = json.load(f)
        ALL_CHAR = init_game_pool('onmyoji', azur_dict, OnmyojiChar)


onmyoji_star = {
    5: 'SP',
    4: 'SSR',
    3: 'SR',
    2: 'R',
}


# 抽取卡池
def _get_onmyoji_card():
    global ALL_CHAR
    star = get_star([5, 4, 3, 2], [ONMYOJI_SP, ONMYOJI_SSR, ONMYOJI_SR, ONMYOJI_R])
    chars = [x for x in ALL_CHAR if x.star == onmyoji_star[star] and not x.limited]
    return random.choice(chars), 5 - star





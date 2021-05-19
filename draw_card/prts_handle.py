import ujson as json
import os
from nonebot.adapters.cqhttp import MessageSegment
import nonebot
import random
from .config import PRTS_FIVE_P, PRTS_FOUR_P, PRTS_SIX_P, DRAW_PATH
from .update_game_info import update_info
from .util import generate_img, init_star_rst, max_card
from .init_card_pool import init_game_pool
from pathlib import Path
from .announcement import PrtsAnnouncement

driver: nonebot.Driver = nonebot.get_driver()

up_char_file = Path() / "data" / "draw_card" / "draw_card_up" / "prts_up_char.json"

up_char_dict = {}
prts_dict = {}
FIVE_LIST = []
FOUR_LIST = []
SIX_LIST = []
THREE_LIST = []
_current_pool_title = ''


async def prts_draw(count: int = 300):
    cnlist = ['★★★★★★', '★★★★★', '★★★★', '★★★']
    operator_list, operator_dict, six_list, star_list, six_olist = _format_card_information(count)
    up_list = []
    if _current_pool_title:
        for key in up_char_dict.keys():
            for value in up_char_dict[key].values():
                for i in value:
                    up_list.append(i)
    rst = init_star_rst(star_list, cnlist, six_list, six_olist, up_list)
    if count > 90:
        operator_list = set(operator_list)
    pool_info = "当前up池: " if _current_pool_title else ""
    return pool_info + _current_pool_title + MessageSegment.image("base64://" + await generate_img(operator_list, 'prts', star_list, [SIX_LIST, FIVE_LIST, FOUR_LIST]))\
           + '\n' + rst[:-1] + '\n' + max_card(operator_dict)


async def update_prts_info():
    global prts_dict, SIX_LIST, FOUR_LIST, FIVE_LIST, THREE_LIST
    url = 'https://wiki.biligame.com/arknights/干员数据表'
    data, code = await update_info(url, 'prts', ['头像', '名称', '阵营', '星级', '性别', '是否感染', '初始生命', '初始防御',
                                                 '初始法抗', '再部署', '部署费用', '阻挡数', '攻击速度', '标签'])
    if code == 200:
        prts_dict = data
        SIX_LIST, FIVE_LIST, FOUR_LIST, THREE_LIST = init_game_pool('prts', data)


@driver.on_startup
async def init_data():
    global prts_dict, SIX_LIST, FIVE_LIST, FOUR_LIST, THREE_LIST
    if not os.path.exists(DRAW_PATH + 'prts.json'):
        await update_prts_info()
    else:
        with open(DRAW_PATH + 'prts.json', 'r', encoding='utf8') as f:
            prts_dict = json.load(f)
        SIX_LIST, FIVE_LIST, FOUR_LIST, THREE_LIST = init_game_pool('prts', prts_dict)
    await _init_up_char()


# 抽取干员
def _get_operator_card():
    global up_char_dict
    rand = random.random()
    if rand <= PRTS_SIX_P:
        operator = _get_up_operator('6')
        if operator:
            return operator, 0
        return random.choice(SIX_LIST), 0
    elif rand <= PRTS_FIVE_P:
        operator = _get_up_operator('5')
        if operator:
            return operator, 1
        return random.choice(FIVE_LIST), 1
    elif rand <= PRTS_FOUR_P:
        operator = _get_up_operator('4')
        if operator:
            return operator, 2
        return random.choice(FOUR_LIST), 2
    else:
        return random.choice(THREE_LIST), 3


# 获得up干员
def _get_up_operator(star: str):
    # print(up_char_dict)
    if _current_pool_title and up_char_dict and up_char_dict[star]:
        rand = random.random()
        # print(f'rand: {rand}')
        for probability in up_char_dict[star].keys():
            if probability < 1:
                if rand < probability:
                    return random.choice(up_char_dict[star][probability])
            else:
                if rand < 1 / float(len(SIX_LIST) + len(up_char_dict[star][probability])) * probability:
                    return random.choice(up_char_dict[star][probability])
    return None


# 整理抽卡数据
def _format_card_information(count: int):
    operator_list = []  # 抽取的干员列表
    operator_dict = {}  # 抽取各干员次数
    star_list = [0, 0, 0, 0]    # 各个星级次数
    six_list = []   # 六星干员列表
    six_olist = []  # 六星干员获取位置
    for i in range(count):
        name, code = _get_operator_card()
        star_list[code] += 1
        if code == 0:
            six_list.append(name)
            six_olist.append(i)
        try:
            operator_dict[name] += 1
        except KeyError:
            operator_dict[name] = 1
        operator_list.append(name)
    return operator_list, operator_dict, six_list, star_list, six_olist


# 获取up干员和概率
async def _init_up_char():
    global up_char_dict, SIX_LIST, FIVE_LIST, FOUR_LIST, _current_pool_title
    up_char_dict = await PrtsAnnouncement().update_up_char()
    print(up_char_dict)
    if _current_pool_title == up_char_dict['title']:
        return
    _current_pool_title = up_char_dict['title']
    up_char_dict = up_char_dict['up_char']
    print('成功获取明日方舟当前up信息...')
    average_dict = {'6': {}, '5': {}, '4': {}}
    for star in up_char_dict.keys():
        for key in up_char_dict[star].keys():
            if average_dict[star].get(up_char_dict[star][key]):
                average_dict[star][up_char_dict[star][key]].append(key)
            else:
                average_dict[star][up_char_dict[star][key]] = [key]
    up_char_dict = {'6': {}, '5': {}, '4': {}}
    for star in average_dict.keys():
        for key in average_dict[star].keys():
            try:
                if not up_char_dict[star].get(float(key) / 100):
                    up_char_dict[star][float(key) / 100] = average_dict[star][key]
            except ValueError:
                up_char_dict[star][int(key[1:])] = average_dict[star][key]


async def reload_pool():
    await _init_up_char()







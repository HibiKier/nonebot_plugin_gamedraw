import ujson as json
import os
from util.init_result import image
from configs.path_config import DRAW_PATH
import nonebot
import random
from .config import PRTS_FIVE_P, PRTS_FOUR_P, PRTS_SIX_P
from .update_game_info import update_info
from .util import generate_img, init_star_rst, max_card

driver: nonebot.Driver = nonebot.get_driver()

prts_dict = {}
FIVE_LIST = []
FOUR_LIST = []
SIX_LIST = []
THREE_LIST = []


async def prts_draw(count: int = 300):
    cnlist = ['★★★★★★', '★★★★★', '★★★★', '★★★']
    operator_list, operator_dict, six_list, star_list, six_olist = _format_card_information(count)
    rst = init_star_rst(star_list, cnlist, six_list, six_olist)
    if count > 50:
        operator_list = set(operator_list)
    return image(b64=await generate_img(operator_list, 'prts', star_list, [SIX_LIST, FIVE_LIST, FOUR_LIST]))\
           + '\n' + rst[:-1] + '\n' + max_card(operator_dict)


async def update_prts_info():
    global prts_dict, SIX_LIST, FOUR_LIST, FIVE_LIST, THREE_LIST
    url = 'https://wiki.biligame.com/arknights/干员数据表'
    data, code = await update_info(url, 'prts', ['头像', '名称', '阵营', '星级', '性别', '是否感染', '初始生命', '初始防御',
                                                 '初始法抗', '再部署', '部署费用', '阻挡数', '攻击速度', '标签'])
    if code == 200:
        prts_dict = data
        SIX_LIST = [prts_dict[name]['名称'] for name in prts_dict if prts_dict[name]['星级'] == '6']
        FIVE_LIST = [prts_dict[name]['名称'] for name in prts_dict if prts_dict[name]['星级'] == '5']
        FOUR_LIST = [prts_dict[name]['名称'] for name in prts_dict if prts_dict[name]['星级'] == '4']
        THREE_LIST = [prts_dict[name]['名称'] for name in prts_dict if prts_dict[name]['星级'] == '3']


@driver.on_startup
async def init_data():
    global prts_dict, SIX_LIST, FIVE_LIST, FOUR_LIST, THREE_LIST
    if not os.path.exists(DRAW_PATH + 'prts.json'):
        await update_prts_info()
    else:
        with open(DRAW_PATH + 'prts.json', 'r', encoding='utf8') as f:
            prts_dict = json.load(f)
            SIX_LIST = [prts_dict[name]['名称'] for name in prts_dict if prts_dict[name]['星级'] == '6']
            FIVE_LIST = [prts_dict[name]['名称'] for name in prts_dict if prts_dict[name]['星级'] == '5']
            FOUR_LIST = [prts_dict[name]['名称'] for name in prts_dict if prts_dict[name]['星级'] == '4']
            THREE_LIST = [prts_dict[name]['名称'] for name in prts_dict if prts_dict[name]['星级'] == '3']


# 抽取干员
def _get_operator_card():
    rand = random.random()
    if rand <= PRTS_SIX_P:
        return random.choice(SIX_LIST), 0
    elif rand <= PRTS_FIVE_P:
        return random.choice(FIVE_LIST), 1
    elif rand <= PRTS_FOUR_P:
        return random.choice(FOUR_LIST), 2
    else:
        return random.choice(THREE_LIST), 3


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








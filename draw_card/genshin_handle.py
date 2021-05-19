import ujson as json
import os
from nonebot.adapters.cqhttp import MessageSegment
import nonebot
import random
from .update_game_info import update_info
from .util import generate_img, init_star_rst
from .config import GENSHIN_FIVE_P, GENSHIN_G_FIVE_P, GENSHIN_FOUR_P, I72_ADD, DRAW_PATH

driver: nonebot.Driver = nonebot.get_driver()

genshin_dict = {}
genshin_arm_dict = {}
FIVE_C_LIST = []
FIVE_ARMS_LIST = []
FOUR_C_LIST = []
FOUR_ARMS_LIST = []
THREE_ARMS_LIST = []

genshin_five = {}
genshin_count = {}
genshin_pl_count = {}


async def genshin_draw(user_id: int, count: int):
    #                   0      1      2
    cnlist = ['★★★★★', '★★★★', '★★★']
    genshin_list, five_list, five_olist, five_dict, star_list = _format_card_information(count, user_id)
    rst = init_star_rst(star_list, cnlist, five_list, five_olist)
    print(five_list)
    temp = ''
    if count > 90:
        genshin_list = set(genshin_list)
    return MessageSegment.image("base64://" + await generate_img(genshin_list, 'genshin', star_list)) + '\n' + rst[:-1] + \
           temp[:-1] + f'\n距离保底发还剩 {90 - genshin_count[user_id] if genshin_count.get(user_id) else "^"} 抽' \
           + "\n【五星：0.6%，四星：5.1%\n第72抽开始五星概率每抽加0.585%】"


async def update_genshin_info():
    global genshin_dict, genshin_arm_dict, FIVE_ARMS_LIST, FIVE_C_LIST, FOUR_ARMS_LIST, FOUR_C_LIST, THREE_ARMS_LIST
    url = 'https://wiki.biligame.com/ys/角色筛选'
    data, code = await update_info(url, 'genshin')
    if code == 200:
        genshin_dict = data
        FIVE_C_LIST = [genshin_dict[name]['名称'] for name in genshin_dict if
                       genshin_dict[name]['稀有度'] == '5星' and genshin_dict[name]['名称'] != '旅行者']
        FOUR_C_LIST = [genshin_dict[name]['名称'] for name in genshin_dict if genshin_dict[name]['稀有度'] == '4星']
    url = 'https://wiki.biligame.com/ys/武器图鉴'
    data, code = await update_info(url, 'genshin_arm', ['头像', '名称', '类型', '稀有度.alt', '初始基础属性1',
                                                        '初始基础属性2', '攻击力（MAX）', '副属性（MAX）', '技能'])
    if code == 200:
        genshin_arm_dict = data
        FIVE_ARMS_LIST = [genshin_arm_dict[name]['名称'] for name in genshin_arm_dict if
                          genshin_arm_dict[name]['稀有度'] == '5星']
        FOUR_ARMS_LIST = [genshin_arm_dict[name]['名称'] for name in genshin_arm_dict if
                          genshin_arm_dict[name]['稀有度'] == '4星']
        THREE_ARMS_LIST = [genshin_arm_dict[name]['名称'] for name in genshin_arm_dict if
                           genshin_arm_dict[name]['稀有度'] == '3星']


# asyncio.get_event_loop().run_until_complete(update_genshin_info())


@driver.on_startup
async def init_data():
    global genshin_dict, genshin_arm_dict, FIVE_ARMS_LIST, FIVE_C_LIST, FOUR_ARMS_LIST, FOUR_C_LIST, THREE_ARMS_LIST
    if not os.path.exists(DRAW_PATH + 'genshin.json') or not os.path.exists(DRAW_PATH + 'genshin_arm.json'):
        await update_genshin_info()
    else:
        with open(DRAW_PATH + 'genshin.json', 'r', encoding='utf8') as f:
            genshin_dict = json.load(f)
        with open(DRAW_PATH + 'genshin_arm.json', 'r', encoding='utf8') as f:
            genshin_arm_dict = json.load(f)
        FIVE_C_LIST = [genshin_dict[name]['名称'] for name in genshin_dict if
                       genshin_dict[name]['稀有度'] == '5星' and genshin_dict[name]['名称'] != '旅行者']
        FIVE_ARMS_LIST = [genshin_arm_dict[name]['名称'] for name in genshin_arm_dict if
                          genshin_arm_dict[name]['稀有度'] == '5星']
        FOUR_C_LIST = [genshin_dict[name]['名称'] for name in genshin_dict if genshin_dict[name]['稀有度'] == '4星']
        FOUR_ARMS_LIST = [genshin_arm_dict[name]['名称'] for name in genshin_arm_dict if
                          genshin_arm_dict[name]['稀有度'] == '4星']
        THREE_ARMS_LIST = [genshin_arm_dict[name]['名称'] for name in genshin_arm_dict if
                           genshin_arm_dict[name]['稀有度'] == '3星']


# 抽取卡池
def _get_genshin_card(mode: int = 1, add: float = 0.0):
    rand = random.random()
    # 普通抽
    if mode == 1:
        if rand <= GENSHIN_FIVE_P + add:
            if random.random() < 0.5:
                return random.choice(FIVE_C_LIST), 0
            else:
                return random.choice(FIVE_ARMS_LIST), 0
        elif rand <= GENSHIN_FOUR_P:
            return random.choice(FOUR_C_LIST + FOUR_ARMS_LIST), 1
        else:
            return random.choice(THREE_ARMS_LIST), 2
    # 十连保底抽
    elif mode == 2:
        if rand <= GENSHIN_G_FIVE_P + add:
            if random.random() < 0.5:
                return random.choice(FIVE_C_LIST), 0
            else:
                return random.choice(FIVE_ARMS_LIST), 0
        else:
            return random.choice(FOUR_C_LIST + FOUR_ARMS_LIST), 1
    # 大保底
    elif mode == 3:
        if random.random() < 0.5:
            return random.choice(FIVE_C_LIST), 0
        else:
            return random.choice(FIVE_ARMS_LIST), 0


def _format_card_information(_count: int, user_id):
    genshin_list = []
    star_list = [0, 0, 0]
    five_olist = []
    five_list = []
    five_dict = {}
    add = 0.0
    if genshin_count.get(user_id) and _count <= 90:
        f_count = genshin_count[user_id]
    else:
        f_count = 0
    if genshin_pl_count.get(user_id) and _count <= 90:
        count = genshin_pl_count[user_id]
    else:
        count = 0
    for i in range(_count):
        count += 1
        f_count += 1
        # 十连保底
        if count == 10 and f_count != 90:
            if f_count >= 72:
                add += I72_ADD
            name, code = _get_genshin_card(2, add)
            count = 0
        # 大保底
        elif f_count == 90:
            name, code = _get_genshin_card(3)
        else:
            if f_count >= 72:
                add += I72_ADD
            name, code = _get_genshin_card(add=add)
            if code == 1:
                count = 0
        star_list[code] += 1
        if code == 0:
            if _count <= 90:
                genshin_five[user_id] = f_count
            add = 0.0
            f_count = 0
            five_list.append(name)
            five_olist.append(i)
            try:
                five_dict[name] += 1
            except KeyError:
                five_dict[name] = 1
        genshin_list.append(name)
    if _count <= 90:
        genshin_count[user_id] = f_count
        genshin_pl_count[user_id] = count
    return genshin_list, five_list, five_olist, five_dict, star_list


def reset_count(user_id: int):
    genshin_count[user_id] = 0
    genshin_pl_count[user_id] = 0


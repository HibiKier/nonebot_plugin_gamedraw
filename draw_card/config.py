import nonebot
from pathlib import Path

try:
    import ujson as json
except ModuleNotFoundError:
    import json

DRAW_PATH = str(Path("data/draw_card/").absolute()) + '/'

# 方舟概率
PRTS_SIX_P = 0.02
PRTS_FIVE_P = 0.08
PRTS_FOUR_P = 0.48
PRTS_THREE_P = 0.42

# 原神概率
GENSHIN_FIVE_P = 0.006
GENSHIN_FOUR_P = 0.051
GENSHIN_THREE_P = 0.43
GENSHIN_G_FIVE_P = 0.016
GENSHIN_G_FOUR_P = 0.13
I72_ADD = 0.0585

# 赛马娘概率
PRETTY_THREE_P = 0.03
PRETTY_TWO_P = 0.18
PRETTY_ONE_P = 0.79

# 坎公骑冠剑
GUARDIAN_THREE_CHAR_P = 0.0275
GUARDIAN_TWO_CHAR_P = 0.19
GUARDIAN_ONE_CHAR_P = 0.7825
# UP角色
GUARDIAN_THREE_CHAR_UP_P = 0.01375
GUARDIAN_THREE_CHAR_OTHER_P = 0.01375

GUARDIAN_EXCLUSIVE_ARMS_P = 0.03
GUARDIAN_FIVE_ARMS_P = 0.03
GUARDIAN_FOUR_ARMS_P = 0.09
GUARDIAN_THREE_ARMS_P = 0.27
GUARDIAN_TWO_ARMS_P = 0.58
# UP武器
GUARDIAN_EXCLUSIVE_ARMS_UP_P = 0.01
GUARDIAN_EXCLUSIVE_ARMS_OTHER_P = 0.02

path_dict = {
    'genshin': '原神',
    'prts': '明日方舟',
    'pretty': '赛马娘',
    'guardian': '坎公骑冠剑',
}

_draw_config = Path() / "data" / "draw_card" / "draw_card_config" / "draw_card_config.json"

driver: nonebot.Driver = nonebot.get_driver()


@driver.on_startup
def check_config():
    global PRTS_SIX_P, PRTS_FOUR_P, PRTS_FIVE_P, PRTS_THREE_P, GENSHIN_G_FIVE_P, \
        GENSHIN_G_FOUR_P, GENSHIN_FOUR_P, GENSHIN_FIVE_P, I72_ADD, path_dict, PRETTY_THREE_P, \
        PRETTY_ONE_P, PRETTY_TWO_P, GENSHIN_THREE_P, GUARDIAN_THREE_CHAR_P, GUARDIAN_TWO_CHAR_P, GUARDIAN_ONE_CHAR_P, \
        GUARDIAN_THREE_CHAR_UP_P, GUARDIAN_THREE_CHAR_OTHER_P, GUARDIAN_EXCLUSIVE_ARMS_P, GUARDIAN_FIVE_ARMS_P, \
        GUARDIAN_FOUR_ARMS_P, GUARDIAN_THREE_ARMS_P, GUARDIAN_TWO_ARMS_P,\
        GUARDIAN_EXCLUSIVE_ARMS_UP_P, GUARDIAN_EXCLUSIVE_ARMS_OTHER_P
    if _draw_config.exists():
        data = json.load(open(_draw_config, 'r', encoding='utf8'))
        PRTS_SIX_P = float(data['prts']['six'])
        PRTS_FIVE_P = float(data['prts']['five'])
        PRTS_FOUR_P = float(data['prts']['four'])
        PRTS_THREE_P = float(data['prts']['three'])

        GENSHIN_FIVE_P = float(data['genshin']['five_char'])
        GENSHIN_FOUR_P = float(data['genshin']['four_char'])
        GENSHIN_THREE_P = float(data['genshin']['three_char'])
        GENSHIN_G_FIVE_P = float(data['genshin']['five_weapon'])
        GENSHIN_G_FOUR_P = float(data['genshin']['four_weapon'])
        I72_ADD = float(data['genshin']['72_add'])

        PRETTY_THREE_P = float(data['pretty']['three'])
        PRETTY_TWO_P = float(data['pretty']['two'])
        PRETTY_ONE_P = float(data['pretty']['one'])

        GUARDIAN_THREE_CHAR_P = float(data['guardian']['GUARDIAN_THREE_CHAR_P'])
        GUARDIAN_TWO_CHAR_P = float(data['guardian']['GUARDIAN_TWO_CHAR_P'])
        GUARDIAN_ONE_CHAR_P = float(data['guardian']['GUARDIAN_ONE_CHAR_P'])
        GUARDIAN_THREE_CHAR_UP_P = float(data['guardian']['GUARDIAN_THREE_CHAR_UP_P'])
        GUARDIAN_THREE_CHAR_OTHER_P = float(data['guardian']['GUARDIAN_THREE_CHAR_OTHER_P'])
        GUARDIAN_EXCLUSIVE_ARMS_P = float(data['guardian']['GUARDIAN_EXCLUSIVE_ARMS_P'])
        GUARDIAN_FIVE_ARMS_P = float(data['guardian']['GUARDIAN_FIVE_ARMS_P'])
        GUARDIAN_FOUR_ARMS_P = float(data['guardian']['GUARDIAN_FOUR_ARMS_P'])
        GUARDIAN_THREE_ARMS_P = float(data['guardian']['GUARDIAN_THREE_ARMS_P'])
        GUARDIAN_TWO_ARMS_P = float(data['guardian']['GUARDIAN_TWO_ARMS_P'])
        GUARDIAN_EXCLUSIVE_ARMS_UP_P = float(data['guardian']['GUARDIAN_EXCLUSIVE_ARMS_UP_P'])
        GUARDIAN_EXCLUSIVE_ARMS_OTHER_P = float(data['guardian']['GUARDIAN_EXCLUSIVE_ARMS_OTHER_P'])

    else:
        _draw_config.parent.mkdir(parents=True, exist_ok=True)
        data = {
            'path_dict': {
                'genshin': '原神',
                'prts': '明日方舟',
                'pretty': '赛马娘',
                'guardian': '坎公骑冠剑',
            },

            'prts': {
                'six': 0.02,
                'five': 0.08,
                'four': 0.48,
                'three': 0.42,
            },

            'genshin': {
                'five_char': 0.006,
                'four_char': 0.051,
                'three_char': 0.43,
                'five_weapon': 0.13,
                'four_weapon': 0.016,
                '72_add': 0.0585,
            },

            'pretty': {
                'three': 0.03,
                'two': 0.18,
                'one': 0.79,
            },
            'guardian': {
                'GUARDIAN_THREE_CHAR_P': 0.0275,
                'GUARDIAN_TWO_CHAR_P': 0.19,
                'GUARDIAN_ONE_CHAR_P': 0.7825,

                'GUARDIAN_THREE_CHAR_UP_P': 0.01375,
                'GUARDIAN_THREE_CHAR_OTHER_P': 0.01375,

                'GUARDIAN_EXCLUSIVE_ARMS_P': 0.03,
                'GUARDIAN_FIVE_ARMS_P': 0.03,
                'GUARDIAN_FOUR_ARMS_P': 0.09,
                'GUARDIAN_THREE_ARMS_P': 0.27,
                'GUARDIAN_TWO_ARMS_P': 0.58,

                'GUARDIAN_EXCLUSIVE_ARMS_UP_P': 0.01,
                'GUARDIAN_EXCLUSIVE_ARMS_OTHER_P': 0.02,
            }
        }
    json.dump(data, open(_draw_config, 'w', encoding='utf8'), indent=4, ensure_ascii=False)

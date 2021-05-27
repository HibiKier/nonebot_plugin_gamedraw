import asyncio
import nonebot
import os
from .pcr_handle import update_pcr_info, init_pcr_data
from .azur_handle import update_azur_info, init_azur_data
from .prts_handle import update_prts_info, init_prts_data
from .pretty_handle import update_pretty_info, init_pretty_data
from .guardian_handle import update_guardian_info, init_guardian_data
from .genshin_handle import update_genshin_info, init_genshin_data
from .config import PRTS_FLAG, PRETTY_FLAG, GUARDIAN_FLAG, PCR_FLAG, AZUR_FLAG, GENSHIN_FLAG, DRAW_PATH


driver: nonebot.Driver = nonebot.get_driver()


@driver.on_startup
async def async_update_game():
    tasks = []
    init_lst = []
    if PRTS_FLAG and not os.path.exists(DRAW_PATH + 'prts.json'):
        tasks.append(asyncio.ensure_future(update_prts_info()))

    if PRETTY_FLAG and (not os.path.exists(DRAW_PATH + 'pretty.json') or
                        not os.path.exists(DRAW_PATH + 'pretty_card.json')):
        tasks.append(asyncio.ensure_future(update_pretty_info()))

    if GUARDIAN_FLAG and not os.path.exists(DRAW_PATH + 'guardian.json'):
        tasks.append(asyncio.ensure_future(update_guardian_info()))

    if PCR_FLAG and not os.path.exists(DRAW_PATH + 'pcr.json'):
        tasks.append(asyncio.ensure_future(update_pcr_info()))

    if GENSHIN_FLAG and (not os.path.exists(DRAW_PATH + 'genshin.json') or
                         not os.path.exists(DRAW_PATH + 'genshin_arms.json')):
        tasks.append(asyncio.ensure_future(update_genshin_info()))

    if AZUR_FLAG and not os.path.exists(DRAW_PATH + 'azur.json'):
        tasks.append(asyncio.ensure_future(update_azur_info()))

    await asyncio.gather(*tasks)
    for func in [init_pcr_data, init_pretty_data, init_azur_data,
                 init_prts_data, init_genshin_data, init_guardian_data]:
        await func()







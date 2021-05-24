from nonebot import on_regex, require, on_keyword
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.permission import SUPERUSER
from nonebot.typing import T_State
from .genshin_handle import genshin_draw, update_genshin_info, reset_count
from .prts_handle import update_prts_info, prts_draw, reload_pool
from .pretty_handle import update_pretty_info, pretty_draw
from .guardian_handle import update_guardian_info, guardian_draw
from .update_game_info import update_info
from .util import is_number
import re

scheduler = require('nonebot_plugin_apscheduler').scheduler

prts = on_regex(r'.*?方舟[1-9|一][0-9]{0,2}[抽|井]', priority=5, block=True)
prts_update = on_keyword({'更新方舟信息', '更新明日方舟信息'}, permission=SUPERUSER, priority=1, block=True)
prts_reload = on_keyword({'重载方舟卡池'}, priority=1, block=True)

genshin = on_regex('.*?原神[1-9|一][0-9]{0,2}[抽|井]', priority=5, block=True)
genshin_reset = on_keyword({'重置原神抽卡'}, priority=1, block=True)
genshin_update = on_keyword({'更新原神信息'}, permission=SUPERUSER, priority=1, block=True)

pretty = on_regex('.*?马娘卡?[1-9|一][0-9]{0,2}[抽|井]', priority=5, block=True)
pretty_update = on_keyword({'更新马娘信息', '更新赛马娘信息'}, permission=SUPERUSER, priority=1, block=True)

guardian = on_regex('.*?坎公骑冠剑武?器?[1-9|一][0-9]{0,2}[抽|井]', priority=5, block=True)
guardian_update = on_keyword({'更新坎公骑冠剑信息'}, permission=SUPERUSER, priority=1, block=True)


test = on_keyword({'test'}, permission=SUPERUSER, priority=1, block=True)


@test.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_guardian_info()


@prts.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    if msg in ['方舟一井', '方舟1井']:
        num = 300
    else:
        rmsg = re.search(r'.*?方舟(.*)抽', msg)
        if rmsg and is_number(rmsg.group(1)):
            try:
                num = int(rmsg.group(1))
            except ValueError:
                await prts.finish('必！须！是！数！字！', at_sender=True)
            if num > 300:
                await prts.finish('一井都满不足不了你嘛！快爬开！', at_sender=True)
            if num < 1:
                await prts.finish('虚空抽卡？？？', at_sender=True)
        else:
            return
    print(num)
    await prts.send(await prts_draw(num), at_sender=True)


@prts_reload.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await reload_pool()
    await prts_reload.finish('重载完成！')


@genshin.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    if msg in ['原神一井', '原神1井']:
        num = 180
    else:
        rmsg = re.search(r'.*?原神(.*)抽', msg)
        if rmsg and is_number(rmsg.group(1)):
            try:
                num = int(rmsg.group(1))
            except ValueError:
                await genshin.finish('必！须！是！数！字！', at_sender=True)
            if num > 300:
                await genshin.finish('一井都满不足不了你嘛！快爬开！', at_sender=True)
            if num < 1:
                await genshin.finish('虚空抽卡？？？', at_sender=True)
        else:
            return
    await genshin.send(await genshin_draw(event.user_id, num), at_sender=True)


@genshin_reset.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    reset_count(event.user_id)
    await genshin_reset.send('重置了原神抽卡次数', at_sender=True)


@pretty.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    if msg.find('1井') != -1 or msg.find('一井') != -1:
        num = 200
        if msg.find("卡") == -1:
            pool_name = 'horse'
        else:
            pool_name = 'card'
    else:
        rmsg = re.search(r'.*?马娘(.*)抽', msg)
        if rmsg:
            num = rmsg.group(1)
            if num[0] == '卡':
                num = num[1:]
                pool_name = 'card'
            else:
                pool_name = 'horse'
            if is_number(num):
                try:
                    num = int(num)
                except ValueError:
                    await genshin.finish('必！须！是！数！字！', at_sender=True)
                if num > 200:
                    await genshin.finish('一井都满不足不了你嘛！快爬开！', at_sender=True)
                if num < 1:
                    await genshin.finish('虚空抽卡？？？', at_sender=True)
            else:
                return
    await pretty.send(await pretty_draw(num, pool_name), at_sender=True)


@guardian.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = str(event.get_message()).strip()
    pool_name = 'char'
    if msg.find('1井') != -1 or msg.find('一井') != -1:
        num = 300
        if msg.find('武器') != -1:
            pool_name = 'arms'
    else:
        rmsg = re.search(r'.*?坎公骑冠剑(.*)抽', msg)
        if rmsg:
            num = rmsg.group(1)
            if num.find('武器') != -1:
                pool_name = 'arms'
                num = num.replace('武器', '')
            if is_number(num):
                try:
                    num = int(num)
                except ValueError:
                    await genshin.finish('必！须！是！数！字！', at_sender=True)
                if num > 200:
                    await genshin.finish('一井都满不足不了你嘛！快爬开！', at_sender=True)
                if num < 1:
                    await genshin.finish('虚空抽卡？？？', at_sender=True)
            else:
                return
    await guardian.send(await guardian_draw(num, pool_name), at_sender=True)


@prts_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_prts_info()
    await reload_pool()
    await prts_update.finish('更新完成！')


@genshin_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_genshin_info()
    await genshin_update.finish('更新完成！')


@pretty_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_pretty_info()
    await genshin_update.finish('更新完成！')


@guardian_update.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    await update_guardian_info()
    await genshin_update.finish('更新完成！')


# 更新资源
@scheduler.scheduled_job(
    'cron',
    hour=4,
    minute=1,
)
async def _():
    try:
        await update_prts_info()
    except Exception as e:
        pass
    try:
        await update_genshin_info()
    except Exception as e:
        pass
    try:
        await update_pretty_info()
    except Exception as e:
        pass
    try:
        await update_guardian_info()
    except Exception as e:
        pass


# 每天四点重载up卡池
@scheduler.scheduled_job(
    'cron',
    hour=4,
    minute=1,
)
async def _():
    await reload_pool()



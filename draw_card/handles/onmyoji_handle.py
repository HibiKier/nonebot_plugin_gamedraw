import random
from lxml import etree
from typing import List
from nonebot.log import logger

try:
    import ujson as json
except ModuleNotFoundError:
    import json

from .base_handle import BaseHandle, BaseData
from ..config import draw_config
from ..util import remove_prohibited_str


class OnmyojiChar(BaseData):
    @property
    def star_str(self) -> str:
        return ["N", "R", "SR", "SSR", "SP"][self.star - 1]


class OnmyojiHandle(BaseHandle[OnmyojiChar]):
    def __init__(self):
        super().__init__("onmyoji", "阴阳师")
        self.max_star = 5
        self.config = draw_config.onmyoji
        self.ALL_CHAR: List[OnmyojiChar] = []

    def get_card(self, **kwargs) -> OnmyojiChar:
        star = self.get_star(
            [5, 4, 3, 2],
            [
                self.config.ONMYOJI_SP,
                self.config.ONMYOJI_SSR,
                self.config.ONMYOJI_SR,
                self.config.ONMYOJI_R,
            ],
        )
        chars = [x for x in self.ALL_CHAR if x.star == star and not x.limited]
        return random.choice(chars)

    def format_max_star(self, card_list: List[OnmyojiChar]) -> str:
        rst = ""
        for index, card in enumerate(card_list, start=1):
            if card.star == self.max_star:
                rst += f"第 {index} 抽获取SP {card.name}\n"
            elif card.star == self.max_star - 1:
                rst += f"第 {index} 抽获取SSR {card.name}\n"
        return rst.strip()

    def _init_data(self):
        self.ALL_CHAR = [
            OnmyojiChar(
                name=value["名称"],
                star=["N", "R", "SR", "SSR", "SP"].index(value["星级"]) + 1,
                limited=True
                if key
                in [
                    "奴良陆生",
                    "卖药郎",
                    "鬼灯",
                    "阿香",
                    "蜜桃&芥子",
                    "犬夜叉",
                    "杀生丸",
                    "桔梗",
                    "朽木露琪亚",
                    "黑崎一护",
                    "灶门祢豆子",
                    "灶门炭治郎",
                ]
                else False,
            )
            for key, value in self.load_data().items()
        ]

    async def _update_info(self):
        info = {}
        url = "https://yys.res.netease.com/pc/zt/20161108171335/js/app/all_shishen.json?v74="
        result = await self.get_url(url)
        if not result:
            logger.warning(f"更新 {self.game_name_cn} 出错")
            return
        data = json.loads(result)
        for x in data:
            name = remove_prohibited_str(x["name"])
            member_dict = {
                "id": x["id"],
                "名称": name,
                "星级": x["level"],
            }
            info[name] = member_dict
            # logger.info(f"{name} is update...")
        # 更新头像
        for key in info.keys():
            url = f'https://yys.163.com/shishen/{info[key]["id"]}.html'
            result = await self.get_url(url)
            if not result:
                info[key]["头像"] = ""
                continue
            try:
                dom = etree.HTML(result, etree.HTMLParser())
                avatar = dom.xpath("//div[@class='pic_wrap']/img/@src")[0]
                avatar = "https:" + avatar
                info[key]["头像"] = avatar
            except IndexError:
                info[key]["头像"] = ""
                logger.warning(f"{self.game_name_cn} 获取头像错误 {key}")
        self.dump_data(info)
        logger.info(f"{self.game_name_cn} 更新成功")
        # 下载头像
        for value in info.values():
            await self.download_img(value["头像"], value["名称"])

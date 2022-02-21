import random
from lxml import etree
from typing import List
from PIL import ImageDraw
from urllib.parse import unquote
from nonebot.log import logger

from .base_handle import BaseHandle, BaseData
from ..config import draw_config
from ..util import remove_prohibited_str, cn2py, load_font
from ..create_img import CreateImg


class AzurChar(BaseData):
    itype: str  # 舰娘类型

    @property
    def star_str(self) -> str:
        return ["白", "蓝", "紫", "金"][self.star - 1]


class AzurHandle(BaseHandle[AzurChar]):
    def __init__(self):
        super().__init__("azur", "碧蓝航线")
        self.max_star = 4
        self.config = draw_config.azur
        self.ALL_CHAR: List[AzurChar] = []

    def get_card(self, pool_name: str, **kwargs) -> AzurChar:
        if pool_name == "轻型":
            itype = ["驱逐", "轻巡", "维修"]
        elif pool_name == "重型":
            itype = ["重巡", "战列", "战巡", "重炮"]
        else:
            itype = ["维修", "潜艇", "重巡", "轻航", "航母"]
        star = self.get_star(
            [4, 3, 2, 1],
            [
                self.config.AZUR_FOUR_P,
                self.config.AZUR_THREE_P,
                self.config.AZUR_TWO_P,
                self.config.AZUR_ONE_P,
            ],
        )
        chars = [
            x
            for x in self.ALL_CHAR
            if x.star == star and x.itype in itype and not x.limited
        ]
        return random.choice(chars)

    def generate_card_img(self, card: AzurChar) -> CreateImg:
        sep_w = 5
        sep_t = 5
        sep_b = 20
        w = 100
        h = 100
        bg = CreateImg(w + sep_w * 2, h + sep_t + sep_b)
        frame_path = str(self.img_path / f"{card.star}_star.png")
        frame = CreateImg(w, h, background=frame_path)
        img_path = str(self.img_path / f"{cn2py(card.name)}.png")
        img = CreateImg(w, h, background=img_path)
        # 加圆角
        frame.circle_corner(6)
        img.circle_corner(6)
        bg.paste(img, (sep_w, sep_t), alpha=True)
        bg.paste(frame, (sep_w, sep_t), alpha=True)
        # 加名字
        text = card.name[:6] + "..." if len(card.name) > 7 else card.name
        font = load_font(fontsize=14)
        text_w, text_h = font.getsize(text)
        draw = ImageDraw.Draw(bg.markImg)
        draw.text(
            (sep_w + (w - text_w) / 2, h + sep_t + (sep_b - text_h) / 2),
            text,
            font=font,
            fill=["#808080", "#3b8bff", "#8000ff", "#c90", "#ee494c"][card.star - 1],
        )
        return bg

    def _init_data(self):
        self.ALL_CHAR = [
            AzurChar(
                name=value["名称"],
                star=int(value["星级"]),
                limited=True if "可以建造" not in value["获取途径"] else False,
                itype=value["类型"],
            )
            for value in self.load_data().values()
        ]

    async def _update_info(self):
        info = {}
        # 更新图鉴
        url = "https://wiki.biligame.com/blhx/舰娘图鉴"
        result = await self.get_url(url)
        if not result:
            logger.warning(f"更新 {self.game_name_cn} 出错")
            return
        dom = etree.HTML(result, etree.HTMLParser())
        contents = dom.xpath(
            "//div[@class='resp-tabs-container']/div[@class='resp-tab-content']"
        )
        for index, content in enumerate(contents):
            char_list = content.xpath("./table/tbody/tr[2]/td/div/div/div/div")
            for char in char_list:
                try:
                    name = char.xpath("./a/@title")[0]
                    frame = char.xpath("./div/a/img/@alt")[0]
                    avatar = char.xpath("./a/img/@srcset")[0]
                except IndexError:
                    continue
                member_dict = {
                    "名称": remove_prohibited_str(name),
                    "头像": unquote(str(avatar).split(" ")[-2]),
                    "星级": self.parse_star(frame),
                    "类型": self.parse_type(index),
                }
                info[member_dict["名称"]] = member_dict
        # 更新额外信息
        for key in info.keys():
            url = f"https://wiki.biligame.com/blhx/{key}"
            result = await self.get_url(url)
            if not result:
                info[key]["获取途径"] = []
                logger.warning(f"{self.game_name_cn} 获取额外信息错误 {key}")
                continue
            try:
                dom = etree.HTML(result, etree.HTMLParser())
                time = dom.xpath(
                    "//table[@class='wikitable sv-general']/tbody[1]/tr[4]/td[2]//text()"
                )[0]
                sources = []
                if "无法建造" in time:
                    sources.append("无法建造")
                elif "活动已关闭" in time:
                    sources.append("活动限定")
                else:
                    sources.append("可以建造")
                info[key]["获取途径"] = sources
            except IndexError:
                info[key]["获取途径"] = []
                logger.warning(f"{self.game_name_cn} 获取额外信息错误 {key}")
        self.dump_data(info)
        logger.info(f"{self.game_name_cn} 更新成功")
        # 下载头像
        for value in info.values():
            await self.download_img(value["头像"], value["名称"])
        # 下载头像框
        idx = 1
        BLHX_URL = "https://patchwiki.biligame.com/images/blhx"
        for url in [
            "/1/15/pxho13xsnkyb546tftvh49etzdh74cf.png",
            "/a/a9/k8t7nx6c8pan5vyr8z21txp45jxeo66.png",
            "/a/a5/5whkzvt200zwhhx0h0iz9qo1kldnidj.png",
            "/a/a2/ptog1j220x5q02hytpwc8al7f229qk9.png",
            "/6/6d/qqv5oy3xs40d3055cco6bsm0j4k4gzk.png",
        ]:
            await self.download_img(BLHX_URL + url, f"{idx}_star")
            idx += 1

    @staticmethod
    def parse_star(star: str) -> int:
        if star == "舰娘头像外框普通.png":
            return 1
        elif star == "舰娘头像外框稀有.png":
            return 2
        elif star == "舰娘头像外框精锐.png":
            return 3
        elif star == "舰娘头像外框超稀有.png":
            return 4
        elif star == "舰娘头像外框海上传奇.png":
            return 5
        elif star in [
            "舰娘头像外框最高方案.png",
            "舰娘头像外框决战方案.png",
            "舰娘头像外框超稀有META.png",
            "舰娘头像外框精锐META.png",
        ]:
            return 6
        else:
            return 6

    @staticmethod
    def parse_type(index: int) -> str:
        azur_types = [
            "驱逐",
            "轻巡",
            "重巡",
            "超巡",
            "战巡",
            "战列",
            "航母",
            "航站",
            "轻航",
            "重炮",
            "维修",
            "潜艇",
            "运输",
        ]
        try:
            return azur_types[index]
        except IndexError:
            return azur_types[0]

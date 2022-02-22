import math
import random
import aiohttp
import asyncio
import aiofiles
from datetime import datetime
from pydantic import BaseModel, Extra
from asyncio.exceptions import TimeoutError
from typing import Dict, List, Optional, TypeVar, Generic
from nonebot.adapters.onebot.v11 import Message, MessageSegment
from nonebot.log import logger

try:
    import ujson as json
except ModuleNotFoundError:
    import json

from ..create_img import CreateImg
from ..config import DRAW_PATH, draw_config
from ..util import cn2py


class BaseData(BaseModel, extra=Extra.ignore):
    name: str  # 名字
    star: int  # 星级
    limited: bool  # 限定

    def __eq__(self, other: "BaseData"):
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    @property
    def star_str(self) -> str:
        return "".join(["★" for _ in range(self.star)])


class UpChar(BaseData):
    zoom: float  # up提升倍率


class UpEvent(BaseModel):
    title: str  # up池标题
    pool_img: str  # up池封面
    start_time: Optional[datetime]  # 开始时间
    end_time: Optional[datetime]  # 结束时间
    up_char: List[UpChar]  # up对象


TC = TypeVar("TC", bound="BaseData")


class BaseHandle(Generic[TC]):
    def __init__(self, game_name: str, game_name_cn: str):
        self.game_name = game_name
        self.game_name_cn = game_name_cn
        self.max_star = 1  # 最大星级
        self.data_path = DRAW_PATH
        self.img_path = DRAW_PATH / f"draw_card/{self.game_name}"
        self.up_path = DRAW_PATH / "draw_card_up"
        self.img_path.mkdir(parents=True, exist_ok=True)
        self.up_path.mkdir(parents=True, exist_ok=True)
        self.data_files: List[str] = [f"{self.game_name}.json"]

    def draw(self, count: int, **kwargs) -> Message:
        cards = self.get_cards(count, **kwargs)
        result = self.format_result(cards)
        return MessageSegment.image(self.generate_img(cards)) + result

    # 抽取卡池
    def get_card(self, **kwargs) -> TC:
        raise NotImplementedError

    def get_cards(self, count: int, **kwargs) -> List[TC]:
        return [self.get_card(**kwargs) for _ in range(count)]

    # 获取星级
    @staticmethod
    def get_star(star_list: List[int], probability_list: List[float]) -> int:
        return random.choices(star_list, weights=probability_list, k=1)[0]

    def format_result(self, card_list: List[TC], **kwargs) -> str:
        results = [
            self.format_star_result(card_list, **kwargs),
            self.format_max_star(card_list, **kwargs),
            self.format_max_card(card_list, **kwargs),
        ]
        results = [rst for rst in results if rst]
        return "\n".join(results)

    def format_star_result(self, card_list: List[TC], **kwargs) -> str:
        star_dict: Dict[str, int] = {}  # 记录星级及其次数

        card_list_sorted = sorted(card_list, key=lambda c: c.star, reverse=True)
        for card in card_list_sorted:
            try:
                star_dict[card.star_str] += 1
            except KeyError:
                star_dict[card.star_str] = 1

        rst = ""
        for star_str, count in star_dict.items():
            rst += f"[{star_str}×{count}] "
        return rst.strip()

    def format_max_star(
        self, card_list: List[TC], up_list: List[str] = [], **kwargs
    ) -> str:
        rst = ""
        for index, card in enumerate(card_list, start=1):
            if card.star == self.max_star:
                if card.name in up_list:
                    rst += f"第 {index} 抽获取UP {card.name}\n"
                else:
                    rst += f"第 {index} 抽获取 {card.name}\n"
        return rst.strip()

    def format_max_card(self, card_list: List[TC], **kwargs) -> str:
        card_dict: Dict[TC, int] = {}  # 记录卡牌抽取次数

        for card in card_list:
            try:
                card_dict[card] += 1
            except KeyError:
                card_dict[card] = 1

        max_count = max(card_dict.values())
        max_card = list(card_dict.keys())[list(card_dict.values()).index(max_count)]
        if max_count <= 1:
            return ""
        return f"抽取到最多的是{max_card.name}，共抽取了{max_count}次"

    def generate_img(self, card_list: List[TC], num_per_line: int = 5) -> str:
        if len(card_list) > 90:
            card_list = list(set(card_list))

        card_imgs: List[CreateImg] = []
        for card in card_list:
            card_img = self.generate_card_img(card)
            card_imgs.append(card_img)

        img_w = card_imgs[0].w
        img_h = card_imgs[0].h
        if len(card_imgs) < num_per_line:
            w = img_w * len(card_imgs)
        else:
            w = img_w * num_per_line
        h = img_h * math.ceil(len(card_imgs) / num_per_line)
        img = CreateImg(w, h, img_w, img_h)
        for card_img in card_imgs:
            img.paste(card_img)
        return img.pic2bs4()

    def generate_card_img(self, card: TC) -> CreateImg:
        img = str(self.img_path / f"{cn2py(card.name)}.png")
        return CreateImg(100, 100, background=img)

    def load_data(self, filename: str = "") -> dict:
        if not filename:
            filename = f"{self.game_name}.json"
        filepath = self.data_path / filename
        if not filepath.exists():
            return {}
        with filepath.open("r", encoding="utf8") as f:
            return json.load(f)

    def dump_data(self, data: dict, filename: str = ""):
        if not filename:
            filename = f"{self.game_name}.json"
        filepath = self.data_path / filename
        with filepath.open("w", encoding="utf8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def data_exists(self) -> bool:
        for file in self.data_files:
            if not (self.data_path / file).exists():
                return False
        return True

    def _init_data(self):
        raise NotImplementedError

    def init_data(self):
        try:
            self._init_data()
        except Exception as e:
            logger.warning(f"{self.game_name_cn} 导入角色数据错误：{type(e)}：{e}")

    async def _update_info(self):
        raise NotImplementedError

    def client(self) -> aiohttp.ClientSession:
        headers = {
            "User-Agent": '"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"'
        }
        return aiohttp.ClientSession(headers=headers)

    async def update_info(self):
        try:
            async with asyncio.Semaphore(draw_config.SEMAPHORE):
                async with self.client() as session:
                    self.session = session
                    await self._update_info()
        except Exception as e:
            logger.warning(f"{self.game_name_cn} 更新数据错误：{type(e)}：{e}")
        self.init_data()

    async def get_url(self, url: str) -> str:
        result = ""
        retry = 5
        for i in range(retry):
            try:
                async with self.session.get(url, timeout=10) as response:
                    result = await response.text()
                break
            except TimeoutError:
                logger.warning(f"访问 {url} 超时, 重试 {i + 1}/{retry}")
                await asyncio.sleep(1)
        return result

    async def download_img(self, url: str, name: str) -> bool:
        img_path = self.img_path / f"{cn2py(name)}.png"
        if img_path.exists():
            return True
        try:
            async with self.session.get(url, timeout=10) as response:
                async with aiofiles.open(str(img_path), "wb") as f:
                    await f.write(await response.read())
            return True
        except TimeoutError:
            logger.warning(f"下载 {self.game_name_cn} 图片超时，名称：{name}，url：{url}")
            return False
        except:
            logger.warning(f"下载 {self.game_name_cn} 链接错误，名称：{name}，url：{url}")
            return False

    async def _reload_pool(self) -> Optional[Message]:
        return None

    async def reload_pool(self) -> Optional[Message]:
        try:
            async with self.client() as session:
                self.session = session
                return await self._reload_pool()
        except Exception as e:
            logger.warning(f"{self.game_name_cn} 重载UP池错误：{type(e)}：{e}")

    def reset_count(self, user_id: int) -> bool:
        return False

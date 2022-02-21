import platform
import pypinyin
from pathlib import Path
from PIL import ImageFont
from PIL.ImageFont import FreeTypeFont

dir_path = Path(__file__).parent.absolute()


def cn2py(word) -> str:
    temp = ""
    for i in pypinyin.pinyin(word, style=pypinyin.NORMAL):
        temp += "".join(i)
    return temp


# 移除windows和linux下特殊字符
def remove_prohibited_str(name: str) -> str:
    if platform.system().lower() == "windows":
        tmp = ""
        for i in name:
            if i not in ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]:
                tmp += i
        name = tmp
    else:
        name = name.replace("/", "\\")
    return name


def load_font(fontname: str = "msyh.ttf", fontsize: int = 16) -> FreeTypeFont:
    return ImageFont.truetype(
        str(dir_path / f"resources/fonts/{fontname}"), fontsize, encoding="utf-8"
    )

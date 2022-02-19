import platform
import pypinyin


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

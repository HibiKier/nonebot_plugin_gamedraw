import base64
from io import BytesIO
from pathlib import Path
from PIL import Image, ImageDraw, UnidentifiedImageError
from nonebot.log import logger


class CreateImg:
    def __init__(
        self,
        w: int,
        h: int,
        img_w: int = 0,
        img_h: int = 0,
        background: str = "",
        color="white",
        image_type="RGBA",
        divisor: float = 1,
    ):
        self.w = int(w)
        self.h = int(h)
        self.img_w = int(img_w)
        self.img_h = int(img_h)
        self.current_w = 0
        self.current_h = 0
        if not background:
            self.markImg = Image.new(image_type, (self.w, self.h), color)
        else:
            try:
                if w == 0 and h == 0:
                    self.markImg = Image.open(background)
                    w, h = self.markImg.size
                    if divisor:
                        self.w = int(divisor * w)
                        self.h = int(divisor * h)
                        self.markImg = self.markImg.resize(
                            (self.w, self.h), Image.ANTIALIAS
                        )
                    else:
                        self.w = w
                        self.h = h
                else:
                    self.markImg = Image.open(background).resize(
                        (self.w, self.h), Image.ANTIALIAS
                    )

            except UnidentifiedImageError as e:
                logger.warning(f"无法识别图片 已删除图片，下次更新重新下载... e：{e}")
                Path(background).unlink(missing_ok=True)
                self.markImg = Image.new(image_type, (self.w, self.h), color)
            except FileNotFoundError:
                logger.warning(f"{background} not exists")
                self.markImg = Image.new(image_type, (self.w, self.h), color)

        self.draw = ImageDraw.Draw(self.markImg)
        self.size = self.w, self.h

    # 贴图
    def paste(self, img, pos=None, alpha=False):
        if isinstance(img, CreateImg):
            img = img.markImg
        if self.current_w == self.w:
            self.current_w = 0
            self.current_h += self.img_h
        if not pos:
            pos = (self.current_w, self.current_h)
        if alpha:
            try:
                self.markImg.paste(img, pos, img)
            except ValueError:
                img = img.convert("RGBA")
                self.markImg.paste(img, pos, img)
        else:
            self.markImg.paste(img, pos)
        self.current_w += self.img_w
        return self.markImg

    def circle_corner(self, r: int):
        img = self.markImg.convert("RGBA")
        w, h = img.size
        alpha = img.split()[-1]
        circle = Image.new("L", (r * 2, r * 2), 0)  # 创建黑色方形
        draw = ImageDraw.Draw(circle)
        draw.ellipse((0, 0, r * 2, r * 2), fill=255)  # 黑色方形内切白色圆形
        draw = ImageDraw.Draw(alpha)
        alpha.paste(circle.crop((0, 0, r, r)), (0, 0))  # 左上角
        alpha.paste(circle.crop((r, 0, r * 2, r)), (w - r, 0))  # 右上角
        alpha.paste(circle.crop((r, r, r * 2, r * 2)), (w - r, h - r))  # 右下角
        alpha.paste(circle.crop((0, r, r, r * 2)), (0, h - r))  # 左下角
        img.putalpha(alpha)
        self.markImg = img

    # 转bs4:
    def pic2bs4(self):
        buf = BytesIO()
        self.markImg.save(buf, format="PNG")
        return f"base64://{base64.b64encode(buf.getvalue()).decode()}"

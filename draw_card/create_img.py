from PIL import Image, ImageDraw
import base64
from io import BytesIO


class CreateImg:
    def __init__(self,
                 w,
                 h,
                 img_w=0,
                 img_h=0,
                 color='white',
                 image_type='RGBA',
                 background='',
                 divisor=1):
        self.w = int(w)
        self.h = int(h)
        self.img_w = int(img_w)
        self.img_h = int(img_h)
        self.current_w = 0
        self.current_h = 0
        if not background:
            self.markImg = Image.new(image_type, (self.w, self.h), color)
        else:
            if w == 0 and h == 0:
                self.markImg = Image.open(background)
                w, h = self.markImg.size
                if divisor:
                    self.w = int(divisor * w)
                    self.h = int(divisor * h)
                    self.markImg = self.markImg.resize((self.w, self.h), Image.ANTIALIAS)
                else:
                    self.w = w
                    self.h = h
            else:
                self.markImg = Image.open(background).resize((self.w, self.h), Image.ANTIALIAS)
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

    # 转bs4:
    def pic2bs4(self):
        buf = BytesIO()
        self.markImg.save(buf, format='PNG')
        base64_str = base64.b64encode(buf.getvalue()).decode()
        return base64_str



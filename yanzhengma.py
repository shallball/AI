#coding=utf-8
import random
import string
from PIL import Image, ImageFont, ImageDraw
import numpy as np
import math
from scipy import misc
import os

#字符集

characters = string.digits + string.ascii_letters


class GenerateImageCaptcha(object):

    def __init__(self, width=160, height=60, fonts=None, font_sizes=None):
        self._width = width
        self._height = height
        self._fonts = fonts or [r'C:\Windows\Fonts\Arial.ttf']
        self._font_sizes = font_sizes or (40, 45, 50)
        self._truefonts = []

    @property
    def truefonts(self):
        if self._truefonts:
            return self._truefonts
        self._truefonts = tuple([
            ImageFont.truetype(r'C:\Windows\Fonts\Arial.ttf', s)
            
            for s in self._font_sizes
        ])
        return self._truefonts


    # 曲线噪音
    @staticmethod
    def create_noise_curve(image, color):
        curve_width = random.randint(0, 4)
        if curve_width == 0:
            return image

        w, h = image.size
        x1 = random.randint(0, int(w / 5))
        y1 = random.randint(int(h / 5), h - int(h / 5))
        for i in range(4):
            x2 = x1 + random.randint(int(w / 5), int(w / 2))
            y2 = random.randint(int(h / 5), h - int(h / 5))
            if x2 <= w:
                ImageDraw.Draw(image).line([x1, y1, x2, y2] , fill=color, width=curve_width)
            else:
                x2 = w
            x1, y1 = x2, y2
        return image

    # 点噪音
    @staticmethod
    def create_noise_dots(image, color, width=3, number=30):
        draw = ImageDraw.Draw(image)
        w, h = image.size
        while number:
            x1 = random.randint(0, w)
            y1 = random.randint(0, h)
            draw.line(((x1, y1), (x1 - 1, y1 - 1)), fill=color, width=width)
            number -= 1
        return image

    # 横向扭曲
    def distort_x_img(self, im_array):
        im_height, im_width = im_array.shape[0], im_array.shape[1]

        im_tmp = np.zeros(shape=im_array.shape)
        factor = random.randint(1, 5)

        phase = random.random()
        move_direction = random.choice(['left', 'right'])
        for i in range(im_height):
            dx = factor * math.sin(phase + 2 * math.pi * i / im_height)
            dx = abs(int(dx))
            if move_direction == 'right':
                im_tmp[i, dx:] = im_array[i, :(im_width - dx)]
                im_tmp[i, :dx] = im_array[i, (im_width - dx):]
            else:
                im_tmp[i, :(im_width - dx)] = im_array[i, dx:]
                im_tmp[i, (im_width - dx):] = im_array[i, :dx]
        return im_tmp

    # 纵向扭曲
    def distort_y_img(self, im_array):
        im_height, im_width = im_array.shape[0], im_array.shape[1]
        im_tmp = np.zeros(shape=im_array.shape)
        factor = random.randint(4, 8)
        period = random.randint(1, 3)
        phase = random.random()
        move_direction = random.choice(['up', 'down'])
        for i in range(im_width):
            dx = factor * (phase + math.sin(2 * math.pi * i * period / im_width))
            dx = abs(int(dx))
            if move_direction == 'up':
                im_tmp[:im_height - dx, i] = im_array[dx:im_height, i]
                im_tmp[im_height - dx:, i] = im_array[:dx, i]
            else:
                im_tmp[dx:, i] = im_array[:im_height - dx, i]
                im_tmp[:dx, i] = im_array[im_height - dx:, i]
        return im_tmp

    #旋转文字
    def draw_image_rotate(self, chars, color, background):
        """Create the CAPTCHA image itself.

        :param chars: text to be generated.
        :param color: color of the text.
        :param background: color of the background.

        The color should be a tuple of 3 numbers, such as (0, 255, 255).
        """
        image = Image.new('RGB', (self._width, self._height), background)
        offset = random.randint(8, 16)
        for c in chars:
            font = random.choice(self.truefonts)
            # w, h = draw.textsize(c, font=font)
            w,h = font.getsize(c)
            im = Image.new('RGBA', (w , h),background)
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            ImageDraw.Draw(im).text((0,0), c, font=font, fill=color)
            # rotate
            im = im.rotate(random.uniform(-30, 30),Image.BILINEAR, expand=1)
            # 创建一个与旋转图像大小相同的白色图像填充四角
            fff = Image.new('RGBA', im.size, (255,) * 4)
            # 复合图像
            im = Image.composite(im,fff,im)
            w, h = im.size
            image.paste(im, (offset, int((self._height - h) / 2)))
            offset = offset + w + random.randint(-5,0)
        return image

    #普通文字
    def draw_img(self, chars, color, background):
        image = Image.new('RGB', (self._width, self._height), background)
        draw_im = ImageDraw.Draw(image)
        x, y = random.randint(8, 16), random.randint(8, 12)
        for ch in chars:
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            font = random.choice(self.truefonts)
            draw_im.text(xy=(x, y), text=ch, fill=color, font=font)
            # 字符间隔
            x = x + font.getsize(ch)[0] + random.randint(0, 10)
            y = random.randint(8, 12)
        return image

    def generate_image(self, chars):
        """Generate the image of the given characters.

        :param chars: text to be generated.
        """
        background = (255, 255, 255)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        #创建旋转文字的图片
        # im = self.draw_image_rotate(chars, color, background)
        #创建普通文字的图片
        im = self.draw_img(chars, color, background)
        #绘制噪音点
        # self.create_noise_dots(im, color)
        #绘制噪音曲线
        #self.create_noise_curve(im, color)
        im_array = np.array(im)
        # 横向扭曲
        im_x_distort = self.distort_x_img(im_array)
        # 横向扭曲后再纵向扭曲
        im_y_distort = self.distort_y_img(im_x_distort)
        return np.array(im),im_x_distort,im_y_distort


def generate_captcha():
    #图片的宽度，高度，文字个数
    width, height, n_len = 160, 70, 4
    #生成文字
    random_str = ''.join(random.sample(characters, n_len))
    #字体集合
    fonts = [os.path.join(r'C:\Windows\Fonts', font) for font in ['Arial.ttf', 'Carlito-Regular.ttf', 'DejaVuSans.ttf']]
    #字体大小集合
    font_sizes = range(40, 50)
    #生成图片
    generator = GenerateImageCaptcha(width=width, height=height, font_sizes=font_sizes, fonts=fonts)
    imgs = generator.generate_image(random_str)
    #保存图片
 
    misc.imsave(r'.\image\{}.png'.format(random_str), imgs[2])


if __name__ == '__main__':
    for _ in range(2000):
        generate_captcha()


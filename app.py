#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os

from PIL import Image

class CutImage:
    """
    切割图像类
    """
    def __init__(self, cutting_rate=177, files=[]):
        self.cutting_rate=cutting_rate
        self.img = None
        self.startx = 0
        self.starty = 0
        self.endx = 0
        self.endy = 0
        self.files = files


    def crop_image(self, filename="test.jpg", count=1):
        # 开始截取
        region = self.img.crop((self.startx, self.starty, self.endx, self.endy))
        # 保存图片
        filename = filename.replace("\\", "") # 去除文件名的特殊字符
        filename, ext = filename.rsplit(".", 1) # 从右向左切割文件名，只分割一次。
        image_path = os.path.join(os.path.abspath(".") + "/" + filename)
        exists = os.path.exists(image_path)
        if not exists:
            os.makedirs(image_path)

        file_path = os.path.join(image_path, "{}.{}".format(count, ext))
        exists = os.path.exists(file_path)
        if exists:
            os.remove(file_path)
        region.save(file_path)


    def generate_image(self):
        for filename in self.files:
            self.img = Image.open(filename)
            img_size = self.img.size
            height = img_size[1]
            width = img_size[0]

            x_dist = [dist for dist in range(1, width) if (dist % self.cutting_rate == 0)]
            x_dist.insert(0, 0)
            y_dist = [dist for dist in range(1, height) if (dist % self.cutting_rate == 0)]
            y_dist.insert(0, 0)

            count = 0 # 文件计数器
            # 先x轴滑动后y轴滑动
            for yDis in y_dist:
                for xDis in x_dist:
                    count += 1
                    self.startx, self.starty, self.endx, self.endy = xDis, yDis, xDis+self.cutting_rate, yDis + self.cutting_rate
                    if self.endx > width:
                        self.endx = width
                    if self.endy > height:
                        self.endy = height
                    self.crop_image(filename=filename, count=count)


def run():
    """
    1. 生成一个截图对象
    2. 传递两个参数
        str cutting_rate: 切割范围-正方向 
        list files: 传入的图片文件列表
    """
    cut_image = CutImage(cutting_rate=177, files=[r"1\11.jpg", r"1\21.jpg", r"1\31.jpg"])
    cut_image.generate_image() # 存到当前目录下，文件名称为files中的文件名加数字 1\11-{int}.jpg

if __name__ == "__main__":
    run()
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import random
import shutil
import glob

from PIL import Image

class CutMultipleImage:
    """
    切割图像类
    """
    def __init__(self, index, files=[]):
        self.img = None
        self.startx = 0
        self.starty = 0
        self.endx = 0
        self.endy = 0
        self.files = files
        self.loc = index


    def crop_image(self, file_path):
        # 开始截取
        region = self.img.crop((self.startx, self.starty, self.endx, self.endy))
        # 保存图片
        exists = os.path.exists(file_path)
        if exists:
            os.remove(file_path)
        region.save(file_path)

    
    def process_file_path(self, index, filename, count):
        filename = filename.replace("\\", "") # 去除文件名的特殊字符
        filename, ext = filename.rsplit(".", 1) # 从右向左切割文件名，只分割一次。

        loc = str(index) + "_" + str(count)
        image_path = os.path.join(os.path.abspath(".") + "/" + loc)
        exists = os.path.exists(image_path)
        if not exists:
            os.makedirs(image_path)
        file_path = os.path.join(image_path, "{}.{}".format(filename, ext))
        return file_path

    def generate_image(self, cutrate):
        rates = []
        for filename in self.files:
            self.img = Image.open(filename)

            img_size = self.img.size
            height = img_size[1]
            width = img_size[0]
            if not rates:
                random_rate = [r for r in range(cutrate, width)]
                rates = random.sample(random_rate, 30)
        
            count = 0 # 文件计数器
            for rate in rates:
                self.cutting_rate = rate
                x_dist = [dist for dist in range(1, width) if (dist % self.cutting_rate == 0)]
                x_dist.insert(0, 0)
                y_dist = [dist for dist in range(1, height) if (dist % self.cutting_rate == 0)]
                y_dist.insert(0, 0)

                # 先x轴滑动后y轴滑动
                for yDis in y_dist:
                    for xDis in x_dist:
                        self.startx, self.starty, self.endx, self.endy = xDis, yDis, xDis+self.cutting_rate, yDis + self.cutting_rate
                        if self.endx <= width and self.endy <= height:
                            count += 1
                            file_path = self.process_file_path(self.loc, filename, count)
                            self.crop_image(file_path)


def run():
    """
    1. 生成一个截图对象
    2. 传递两个参数
        str cutting_rate: 切割范围-正方向 
        list files: 传入的图片文件列表
    """
    cutrate = 177
    Imagefiles = [[r"1.jpg", r"2.jpg"], [r"1.jpg", r"2.jpg"]]
    for index, imagefile in enumerate(Imagefiles):
        loc = str(index) + "_*"
        image_path = os.path.join(os.path.abspath(".") + "/")
        for directory in glob.glob(os.path.join(image_path, loc)):
            shutil.rmtree(directory)
        cut_image = CutMultipleImage(files=imagefile, index=index)
        cut_image.generate_image(cutrate=cutrate) 

if __name__ == "__main__":
    run()

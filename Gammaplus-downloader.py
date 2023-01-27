# Updated : 27 January 2023
# Gammaplus Takeshobo Downloader
# Gammaplus 
# Takeshobo
# https://github.com/SatyamSSJ10

import re
import requests as req
import cv2
import numpy as np
import ast
import os

class Image_Data:
    def __init__(self, link:str, path):
        self.link = link
        self.img_start = 0
        self.img_end = 0
        self.path = path
        if(not os.path.exists(str(path))):
            os.mkdir(str(path))
        os.chdir(path)

    def get_img_names(self) -> None:
        res = req.get(self.link)
        while True:
            if re.search("data/000{}.ptimg.json".format(self.img_start),res.text) is not None:
                break
            else:
                self.img_start = self.img_start + 1
            x = re.findall("data-ptimg=",res.text)
            self.img_end = len(x) + self.img_start #- 1

    def return_image_token_link(self):
        return [self.link +"/data/00{:02}.ptimg.json".format(i) for i in range(self.img_start,self.img_end)]

    def return_image_link(self):
        return [self.link +"/data/00{:02}.jpg".format(i) for i in range(self.img_start,self.img_end)]

    def fetch_images(self):
        j = self.img_start
        token = self.return_image_token_link()
        for i in self.return_image_link():
            image = req.get(i)
            open("temp.jpg", "wb").write(image.content)
            temp_img = cv2.imread("temp.jpg")
            y,x,channels = temp_img.shape
            img = np.zeros((y,x,channels), dtype=np.uint8)
            dataload = ast.literal_eval(req.get(token[self.return_image_link().index(i)]).text)
            dataload_height = int(dataload["views"][0]["height"])
            dataload_width = int(dataload["views"][0]["width"])
            for i in range(64):
                string = dataload["views"][0]["coords"][i]
                list1 = re.split(r'[>+:,]', string)
                #crop_img = temp_img[(int(list1[2])-4):(int(list1[2])-4)+(int(list1[4])+8), (int(list1[1])-4):(int(list1[1])-4)+(int(list1[3])+8)] #The old code
                crop_img = temp_img[(int(list1[2])):(int(list1[2])-4)+(int(list1[4])+8), (int(list1[1])):(int(list1[1])-4)+(int(list1[3])+8)]
                h = int(list1[5])
                k = int(list1[6])
                y,x = crop_img.shape[:2]
                img[k:k+y,h:h+x] = crop_img
            img = img[0:dataload_height+2,0:dataload_width+2]
            cv2.imwrite(dataload["resources"]["i"]["src"], img)
            print("Saved : " + str(dataload["resources"]["i"]["src"]))
            j = j + 1
        os.remove("temp.jpg")

if __name__ == "__main__":
    l1 = Image_Data(str(input(r"Input the link with 'HTTPS://' : ")),str(input(r"Input the absolute path to save : ")))
    l1.get_img_names()
    l1.return_image_token_link()
    l1.return_image_link()
    l1.fetch_images()
    

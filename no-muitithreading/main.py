#!/usr/bin/python
# coding=utf-8
# vim:fileencoding=utf-8

from PIL import Image
import os
import logging
import time

input_dir = "input_img/"
output_dir = "output_img/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
if not os.path.exists("log/"):
    os.makedirs("log/")

log_filename = "run_" + str(int(time.time())) + ".log"
log_filepath = os.path.join("log/", log_filename)
logging.basicConfig(filename=log_filepath, level=logging.INFO)
logger = logging.getLogger("Transcoder")

files = os.listdir(input_dir)
num = 1

for file in files:
    imgpath = os.path.join(input_dir, file)
    try :
        img = Image.open(imgpath)
        basename = os.path.splitext(file)[0] + "_"
        newfile = basename + str(num) + ".jpg"
        output_p = os.path.join(output_dir, newfile)
        img.save(output_p, format="JPG")
        num += 1
        print(f"已轉換 {file} 到 {newfile}")
        logger.info(f"Transcoded {file} to {newfile}")
    except Exception as e:
        print(f"轉換失敗 {file} 原因 {e}")
        logger.error(f"Transcode Error: {e} File: {file}") 


print("已轉換完成")
logger.info("Transcode Completed")
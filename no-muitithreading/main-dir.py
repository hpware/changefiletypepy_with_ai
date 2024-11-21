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

log_filename = "run_dir_" + str(int(time.time())) + ".log"
log_filepath = os.path.join("log/", log_filename)
logging.basicConfig(filename=log_filepath, level=logging.INFO)
logger = logging.getLogger("Transcoder")

files = os.listdir(input_dir)
num = 1
for root, dirs, files in os.walk(input_dir):
    for file in files:
        imgpath = os.path.join(root, file)
        try :
            img = Image.open(imgpath)
            relpath = os.path.relpath(root, input_dir)
            output_sdir = os.path.join(output_dir, relpath)
            if not os.path.exists(output_sdir):
                os.makedirs(output_sdir)
            basename = os.path.splitext(file)[0] + "_"
            newfile = basename + str(num) + ".jpg"
            output_p = os.path.join(output_sdir, newfile)
            img.save(output_p, format="JPG")
            num += 1
            print(f"已轉換 {file} 到 {newfile} in {relpath}")
            logger.info(f"{file} to {newfile} in {relpath}")
        except Exception as e:
            relpath = os.path.relpath(root, input_dir)
            print(f"轉換失敗 {file} in {relpath} 原因 {e}")
            logger.error(f"{e} File: {file} in {relpath}")

print("已轉換完成")
logger.info("Transcode Completed")
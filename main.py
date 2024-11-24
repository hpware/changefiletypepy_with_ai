#!/usr/bin/python
# coding=utf-8
# vim:fileencoding=utf-8

import os
import logging
import time
import requests
import torch
import yaml
import json
import io
from PIL import Image
from concurrent.futures import ThreadPoolExecutor
from transformers import AutoProcessor, AutoModelForCausalLM 


input_dir = "input_img/"
output_dir = "output_img/"
output_dir_yaml = "output_json/"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
if not os.path.exists(input_dir):
    os.makedirs(input_dir)
if not os.path.exists("log/"):
    os.makedirs("log/")
if not os.path.exists(output_dir_yaml): 
    os.makedirs(output_dir_yaml)
log_filename = "run_dir_" + str(int(time.time())) + ".log"
log_filepath = os.path.join("log/", log_filename)
logging.basicConfig(filename=log_filepath, level=logging.INFO)
logger = logging.getLogger("Transcoder")

device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

model = AutoModelForCausalLM.from_pretrained("microsoft/Florence-2-large", torch_dtype=torch_dtype, trust_remote_code=True).to(device)
processor = AutoProcessor.from_pretrained("microsoft/Florence-2-large", trust_remote_code=True)

def process_img(root, file, num):
        imgpath = os.path.join(root, file)
        try :
            img = Image.open(imgpath)
            relpath = os.path.relpath(root, input_dir)
            newfile = str(num) + ".jpg"
            output_p = os.path.join(output_dir, newfile)
            img.save(output_p, format="JPEG")
            print(f"已轉換 {file} 到 {newfile} in {relpath}")
            logger.info(f"{file} to {newfile} in {relpath}")
        except Exception as e:
            relpath = os.path.relpath(root, input_dir)
            print(f"轉換失敗 {file} in {relpath} 原因 {e}")
            logger.error(f"{e} File: {file} in {relpath}")

def processyaml(image, model, processor, device, torch_dtype, num):
    inputs = processor(text="<OD>", images=image, return_tensors="pt").to(device, torch_dtype)

    generated_ids = model.generate(
        input_ids=inputs["input_ids"],
        pixel_values=inputs["pixel_values"],
        max_new_tokens=1024,
        num_beams=3,
        do_sample=False
    )
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=False)[0]

    parsed_answer = processor.post_process_generation(generated_text, task="<OD>", image_size=(image.width, image.height))

    data = [
        {
            "answer": parsed_answer
        }
    ]

    newfile = str(num) + ".json"
    output_p = os.path.join(output_dir_yaml, newfile)
    with io.open(output_p, 'w', encoding='utf8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
    print(f"已產生 {newfile}")
    logger.info(f"Generated {newfile}")

try:
    files = os.listdir(input_dir)
    num = 1
    # First process images
    with ThreadPoolExecutor() as executor:
        features = []
        for root, dirs, files in os.walk(input_dir):
            for file in files: 
                features.append(executor.submit(process_img, root, file, num))
                num += 1
        for feature in features:
            feature.result()
    num = 1
    for oroot, odirs, ofiles in os.walk(output_dir):
        for file in ofiles:
            if file.endswith('.jpg'):
                imgpath = os.path.join(oroot, file)
                image = Image.open(imgpath)
                processyaml(image=image, model=model, processor=processor, 
                          device=device, torch_dtype=torch_dtype, num=num)
                num += 1
    
    print("已轉換完成")
    logger.info("Transcode Completed")
    if os.path.exists("filecount.txt"):
        os.remove("filecount.txt")
    repeat = num
    num = 1
    with open("filecount.txt", "w") as f:
        f.write("[")
        while num != repeat:
            f.write('"'+ str(num) + '"')
            num += 1
            print("已寫入" + str(num))
            if num != repeat:
                f.write(", ")
            else:
                f.write("]")
    logger.info("Filecount updated")
except KeyboardInterrupt:
    print("使用者中斷")
    logger.error("User Interrupt")

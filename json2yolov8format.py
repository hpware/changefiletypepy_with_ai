# coding = UTF-8

import os
import json
import logging
import time

list = ["land vehicle", "airplane", "bicycle", "bus", "motorcycle", "train", "truck"]

log_filename = "run_dir_" + str(int(time.time())) + ".log"
log_filepath = os.path.join("log/", log_filename)
logging.basicConfig(filename=log_filepath, level=logging.INFO)
logger = logging.getLogger("Transcoder")


for files in os.listdir("output_yaml/"):
    for f in files:
        f = os.path.join("output_yaml/", f)
        f = f + ".json"
        with open(f, "r") as file:
                jc = file.read()
                j = json.loads(jc)
                if isinstance(j, list) and len(j) > 0:
                    for i in j:
                        if i["label"] in list:
                            print(i)
                            logger.info(f"{i} in {f}")
                        else:
                            print(f"{i} not in {f}")
                            logger.info(f"{i} not in {f}")
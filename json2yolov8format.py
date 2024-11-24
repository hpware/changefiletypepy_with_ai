# coding = UTF-8

import os
import json
import logging
import time

list1 = ["land vehicle", "airplane", "bicycle", "bus", "motorcycle", "train", "truck"]

log_filename = "run_dir_" + str(int(time.time())) + ".log"
log_filepath = os.path.join("log/", log_filename)
logging.basicConfig(filename=log_filepath, level=logging.INFO)
logger = logging.getLogger("Transcoder")


try:
    with open("filecount.txt", "r") as f:
        filecount = f.read()
        print(filecount)
except Exception as e:
    print(f"Error: {e}")
    logger.error(f"Error: {e}")
    exit()

# try:
#     with open("filecount.txt", "r") as f:
#         lastfile = int(f.read())
#         num = 1
# except Exception as e:
#     print(f"Error: {e}")
#     logger.error(f"Error: {e}")
#     exit()
# if (num != lastfile):
#     f = os.path.join("output_yaml/", str(num) + ".json")
#     with open(f, "r") as file:
#         jc = file.read()
#         j = json.loads(jc)
#         if isinstance(j, list) and len(j) > 0:
#             for i in j:
#                 print(i)


# for files in os.listdir("output_yaml/"):
    #for f in files:
        #f = os.path.join("output_yaml/", f + ".json")
        #with open(f, "r") as file:
                #jc = file.read()
                #j = json.loads(jc)
                #if isinstance(j, list) and len(j) > 0:
                    #for i in j:
                            #print(i)
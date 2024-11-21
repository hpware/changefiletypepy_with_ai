import os 

if not os.path.exists("output_img/"):
    os.makedirs("output_img/")
    print("output_img folder created")
if not os.path.exists("input_img/"):
    os.makedirs("input_img/")
    print("input_img folder created")
if not os.path.exists("log/"):
    os.makedirs("log/")
    print("log folder created")

import os
import random
import datetime
import re
import requests
image_directory = "images"


def getRandomFile(path):
    image_files = os.listdir(path)
    random_image = random.choice(image_files)
    return random_image


print(getRandomFile(image_directory))
print(datetime.datetime.now())


url = "https://www.dmoe.cc/random.php?return=json"
response = requests.get(url)
if response.status_code == 200:
    # 创建用于存储临时图片的目录
    content_type = response.headers.get("content-type", "image/jpeg")
    image_url = response.json()['imgurl']
    image_bytes = requests.get(image_url).content
    file_name = re.search(r'/([^/]+)$', image_url).group(1)
    print("保存文件：" + file_name)
    # 创建一个临时文件，将图片数据写入临时文件
    os.makedirs("temp_images", exist_ok=True)
    temp_file = os.path.join("temp_images", file_name)
    with open(temp_file, "wb") as file:
        file.write(image_bytes)
    

from fastapi import APIRouter, Request, Query
import os
import random
import datetime
from fastapi.staticfiles import StaticFiles
from fastapi.responses import  RedirectResponse
import re
import requests
router = APIRouter(tags=["act_random"])
# 存储图片文件目录
image_directory = "images"

# 存储上次选择的图像的信息
last_selected_image = None
last_selected_day = None
# router.mount('/static', StaticFiles(directory=image_directory), name="static")


def getRandomFile(path):
    image_files = os.listdir(path)
    filtered_image = [file for file in image_files if os.path.isfile(
        os.path.join(path, file))]
    random_image = random.choice(filtered_image)
    return random_image


def select_random_image():
    global last_selected_image, last_selected_day
    current_day = datetime.datetime.now().day

    # 如果上次选择的图像日期与今天不同，或者尚未选择图像，则选择一个新的随机图像
    if last_selected_day != current_day or last_selected_image is None:
        last_selected_image = getRandomFile(image_directory)
        last_selected_day = current_day
    return last_selected_image



@router.get("/acg", description="获取随机图的url,json或者image格式返回")
async def get_random_image(request: Request, type: str = Query(default='image', description="type参数用于设置返回类型")):
    global image_directory
    random_image = getRandomFile(image_directory)
    image_url = request.url_for("img", path=random_image)._url

    if type == 'image':
        return RedirectResponse(image_url)
    if type == 'json':
        return {
            "state": "success",
            "image_url": image_url
        }
    return {
        "state": "Error",
        "info": "请修改请求类型"
    }


@router.get('/acg_day', description="获取今日随机图")
async def get_random_image(request: Request, type: str = Query(default='image', title="获取类型/json/image", description="type参数用于设置返回类型")):
    random_image = select_random_image()
    image_url = request.url_for("img", path=random_image)._url
    if type == 'image':
        return RedirectResponse(image_url)
    if type == 'json':
        return {
            "random_image": image_url
        }
    return {
        "state": "Error",
        "info": "请修改请求类型"
    }


@router.get('/download')
async def get_sakura_acg_random_images():
    sakura_url = "https://www.dmoe.cc/random.php?return=json"
    response = requests.get(sakura_url)
    if response.status_code == 200:
        image_url = response.json()['imgurl']
        image_bytes = requests.get(image_url).content
        file_name = re.search(r'/([^/]+)$', image_url).group(1)
        print("保存文件：" + file_name)
        # 创建一个临时文件，将图片数据写入临时文件
        os.makedirs("images", exist_ok=True)
        temp_file = os.path.join("images", file_name)
        with open(temp_file, "wb") as file:
            file.write(image_bytes)
        return {
            "downloadinfo": "success",
            "file_url": f"{image_url}"
        }
    else:
        return {
            "downloadinfo": "failed"
        }


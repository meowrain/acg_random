from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
import requests
import os
import random
import datetime
import re
app = FastAPI(title="Random ACG Pictures", version='1',
              summary="一个简单得随机图API，Created by meowrain", description="欢迎来到Meowrain得随机图API网站，下面是API请求的使用方法",docs_url=None, redoc_url=None)

# 存储图片文件目录
image_directory = "images"

# 存储上次选择的图像的信息
last_selected_image = None
last_selected_day = None
app.mount('/static', StaticFiles(directory=image_directory), name="static")


def getRandomFile(path):
    image_files = os.listdir(path)
    random_image = random.choice(image_files)
    return random_image


def select_random_image():
    global last_selected_image, last_selected_day
    current_day = datetime.datetime.now().day

    # 如果上次选择的图像日期与今天不同，或者尚未选择图像，则选择一个新的随机图像
    if last_selected_day != current_day or last_selected_image is None:
        last_selected_image = getRandomFile(image_directory)
        last_selected_day = current_day
    return last_selected_image

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/js/swagger-ui-bundle.js",
        swagger_css_url="/static/css/swagger-ui.css",
    )

@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/", description="返回到文档主页")
async def home() -> RedirectResponse:
    return RedirectResponse("/docs")




@app.get("/acg", description="获取随机图的url,json或者image格式返回")
async def get_random_image(request: Request, type: str = Query(default='image', description="type参数用于设置返回类型")):
    global image_directory
    random_image = getRandomFile(image_directory)
    image_url = request.url_for("static", path=random_image)._url

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


@app.get('/acg_day', description="获取今日随机图")
async def get_random_image(request: Request, type: str = Query(default='image', title="获取类型/json/image", description="type参数用于设置返回类型")):
    random_image = select_random_image()
    image_url = request.url_for("static", path=random_image)._url
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

@app.get('/sakura_acg')
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
from fastapi import FastAPI, Request, Query, UploadFile
import uvicorn
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from routers import acg_random,home,upload_file
from middleware import cors
app = FastAPI(title="Random ACG Pictures", version='1',
              summary="一个简单得随机图API，Created by meowrain", description="欢迎来到Meowrain得随机图API网站，下面是API请求的使用方法", docs_url=None, redoc_url=None)

# 挂载路由
app.include_router(acg_random.router)
app.include_router(home.router)
app.include_router(upload_file.router)

# cors跨域
cors.relieve_cors(app)

# 静态文件配置
static_files = "assets"
app.mount('/static', StaticFiles(directory=static_files), name="static") # css/js文件
app.mount('/img',StaticFiles(directory="images"),name="img") # 随机图
app.mount('/upload',StaticFiles(directory="upload"),name="upload") #上传图床


# docs处理
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


if __name__ == '__main__':
    uvicorn.run(app="main:app", host="0.0.0.0", port=8888, reload=True)

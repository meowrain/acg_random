from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
def relieve_cors(app:FastAPI):
    # 设置取消跨域请求
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
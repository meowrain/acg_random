'''
Author: meowrain meowrain@126.com
Date: 2023-11-05 21:15:13
LastEditors: meowrain meowrain@126.com
LastEditTime: 2023-11-06 00:20:33
FilePath: \acg_random\convert_markdown_html\app\app.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os
import uvicorn
from convert import convert_md
app = FastAPI()
app.mount("/static", StaticFiles(directory="./convert/web"), name="static")
templates = Jinja2Templates(directory="templates")

def getHTMLlinks():
    files_list = []
    for entry in os.scandir("./convert/web"):
        if entry.is_file() and entry.name.endswith(".html"):
            files_list.append(entry.name)
    
    html_links = []
    for file_name in files_list:
        file_name = file_name.split('.')[0]
        html_links.append(file_name)
    return html_links

def getMarkdownPostNameWithLinks():
    titles = []
    links = getHTMLlinks()
    for entry in os.scandir("./convert/files"):
        if entry.is_file() and entry.name.endswith(".md"):
            with open(entry.path, "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith("# "):
                        title = line[2:].strip()
                        titles.append(title)
                        break  # 跳出内层循环，继续遍历其他文件
    title_links_dict = {title: link for title, link in zip(titles, links)}
    return title_links_dict
    
@app.get("/")
async def read_root(request: Request,response_class=HTMLResponse):
    convert_md()
    
    titlesAndLinks = getMarkdownPostNameWithLinks()
    return templates.TemplateResponse("index.html", {"request": request,"content":titlesAndLinks})

@app.get("/posts")
def get_posts(request: Request,url:str,response_class=HTMLResponse):
    return templates.TemplateResponse("content.html", {"request": request, "html_content": url})
if __name__ == '__main__':
    uvicorn.run(app="app:app", host="0.0.0.0", port=8888, reload=True)

'''
Author: meowrain meowrain@126.com
Date: 2023-11-05 20:21:44
LastEditors: meowrain meowrain@126.com
LastEditTime: 2023-11-05 21:36:23
FilePath: \acg_random\convert_markdown_html\app\convert\main.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import mistletoe
from mistletoe.latex_renderer import LaTeXRenderer
from .utils import PygmentsRenderer
import os

directory = './convert/files'
files_list = os.listdir(directory)
def convert_md():
    for file in files_list:        
        with open(os.path.join(directory,file),'r',encoding='utf-8') as input_file:
            text = input_file.read()
        html = mistletoe.markdown(text,PygmentsRenderer)
        with open(f'./convert/web/{file.split(".")[0]}.html','w',encoding='utf-8',errors='xmlcharrefreplace') as output_file:
            output_file.write(html)
        print(f'convert {file} over')
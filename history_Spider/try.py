import requests
from bs4 import BeautifulSoup
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
import json
import sys
import time

with open('celebrity.txt', 'r', encoding='utf-8') as file:
    # 逐行读取文件
    for line in file:
        # 去除每行末尾的换行符并打印
        names = line.strip()
        print(names)
        # names=input('请输入一个历史人物的名字:')

        name = parse.urlencode({'name': names})

        url = 'https://baike.baidu.com/item/' + name[name.find('=') + 1:]
# 百度百科页面的URL

        # 发送GET请求
        response = requests.get(url)
        # 检查请求是否成功
        if response.status_code == 200:
            # 使用BeautifulSoup解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
        else:
            print("请求失败，状态码：", response.status_code)
            exit()
        # 定位包含基本信息的div，类名为"basicInfo_spa7J J-basic-info"
        basic_info_div = soup.find('div', class_='basicInfo_spa7J J-basic-info')

        # 检查是否找到该div
        if basic_info_div:
            # 遍历包含具体信息的dl元素
            for dl in basic_info_div.find_all('dl', class_='basicInfoBlock__L35f'):
                for item_wrapper in dl.find_all('div', class_='itemWrapper_RToAN'):
                    dt = item_wrapper.find('dt', class_='basicInfoItem_s_YWZ itemName_Un9Kz')  # 找到标签
                    dd = item_wrapper.find('dd', class_='basicInfoItem_s_YWZ itemValue_sOz6C')  # 找到具体信息

                    # 打印信息
                    if dt and dd:
                        label = dt.get_text(strip=True)
                        value = dd.get_text(strip=True)
                        print(f"{label}: {value}")
        else:
            print("未找到基本信息区域")
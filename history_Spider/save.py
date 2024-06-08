# import requests
# from bs4 import BeautifulSoup
# from urllib import parse
# import json
# import re
#
# data_list = []  # 创建一个空列表，用于存储所有名人的信息
#
# with open('celebrity.txt', 'r', encoding='utf-8') as file:
#     for line in file:
#         names = line.strip()
#         print(names)
#
#         name = parse.urlencode({'name': names})
#         url = 'https://baike.baidu.com/item/' + name[name.find('=') + 1:]
#
#         response = requests.get(url)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, 'html.parser')
#         else:
#             print("请求失败，状态码：", response.status_code)
#             continue  # 如果请求失败，跳过当前循环
#
#         basic_info_div = soup.find('div', class_='basicInfo_spa7J J-basic-info')
#         if basic_info_div:
#             celebrity_data = {}  # 创建一个字典，用于存储当前名人的信息
#             for dl in basic_info_div.find_all('dl', class_='basicInfoBlock__L35f'):
#                 for item_wrapper in dl.find_all('div', class_='itemWrapper_RToAN'):
#                     dt = item_wrapper.find('dt', class_='basicInfoItem_s_YWZ itemName_Un9Kz')
#                     dd = item_wrapper.find('dd', class_='basicInfoItem_s_YWZ itemValue_sOz6C')
#
#                     if dt and dd:
#                         label = dt.get_text(strip=True)
#                         label = re.sub(r'\s+', '', label)
#                         value = dd.get_text(strip=True)
#                         celebrity_data[label] = value  # 将标签和值添加到字典中
#
#             data_list.append(celebrity_data)  # 将当前名人的信息字典添加到列表中
#         else:
#             print("未找到基本信息区域")
#
# # 将列表转换为JSON格式
# json_data = json.dumps(data_list, ensure_ascii=False, indent=4)
#
# # 打印JSON数据或者写入文件
# print(json_data)
# with open('celebrity_info2.json', 'w', encoding='utf-8') as json_file:
#     json_file.write(json_data)
import requests
from bs4 import BeautifulSoup
from urllib import parse
import json
import re

data_list = []  # 创建一个空列表，用于存储所有名人的信息

with open('celebrity_pre.txt', 'r', encoding='utf-8') as file:
    for line in file:
        names = line.strip()
        print(names)

        name = parse.urlencode({'name': names})
        url = 'https://baike.baidu.com/item/' + name[name.find('=') + 1:]

        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
        else:
            print("请求失败，状态码：", response.status_code)
            continue  # 如果请求失败，跳过当前循环

        basic_info_div = soup.find('div', class_='basicInfo_g3agz J-basic-info')
        if basic_info_div:
            celebrity_data = {}  # 创建一个字典，用于存储当前名人的信息

            for dl in basic_info_div.find_all('dl'):
                for item_wrapper in dl.find_all('div', class_='itemWrapper_sMb8G'):
                    dt = item_wrapper.find('dt', class_='basicInfoItem_i0vLA itemName_PrYUb')
                    dd = item_wrapper.find('dd', class_='basicInfoItem_i0vLA itemValue_YsRqx')

                    if dt and dd:
                        label = dt.get_text(strip=True)
                        label = re.sub(r'\s+', '', label)
                        value = dd.get_text(strip=True)
                        celebrity_data[label] = value  # 将标签和值添加到字典中

            data_list.append(celebrity_data)  # 将当前名人的信息字典添加到列表中
        else:
            print("未找到基本信息区域")

# 将列表转换为JSON格式
json_data = json.dumps(data_list, ensure_ascii=False, indent=4)

# 打印JSON数据或者写入文件
print(json_data)
with open('celebrity_info3.json', 'w', encoding='utf-8') as json_file:
    json_file.write(json_data)

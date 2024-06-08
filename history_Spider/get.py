# -*- coding: utf-8 -*-
# @Time     : 2020/1/31 14:40
# @Author   : LiuZe
# @File     : movies.py.py
# @Software : PyCharm



from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
import json
import sys
import time


def Conduct(name_content):  #定义一个函数，用来去除爬取的信息中那些不重要的信息
    name_str = '';name_str_1=''
    j = 0
    for str_1 in name_content:
        if '\u4e00' <= str_1 <= '\u9fff' or str_1 in ['，', '。', '《', '》', '“', '”', '？', '—', '（', '）'] or str_1 in [str(k) for k in range(10)]:
            name_str += str_1
    for str_1 in name_str:
        if str_1 in [str(i) for i in range(10)]:
            j+=1
        else:
            if j>4: # 一般在爬取的内容中，年份最大位数不会超过五位
                name_str_1=name_str_1[:len(name_str_1)-j]
            j=0
        name_str_1 += str_1
    name_str_1=name_str_1[:name_str_1.rfind('。')]
    return name_str_1


# 导入sys和time模块是为了显示进度条

def Time_1():     #  进度条函数
    for i in range(1,51):
        sys.stdout.write('\r')
        sys.stdout.write('{0}% |{1}'.format(int(i%51)*2,int(i%51)*'■'))
        sys.stdout.flush()
        time.sleep(0.125)
    sys.stdout.write('\n')

def search():
    with open('celebrity.txt', 'r', encoding='utf-8') as file:
        # 逐行读取文件
        for line in file:
            # 去除每行末尾的换行符并打印
            names = line.strip()
            print(names)
        # names=input('请输入一个历史人物的名字:')

            name=parse.urlencode({'name':names})

            url='https://baike.baidu.com/item/'+name[name.find('=')+1:]
            print("正在访问的URL:", url)
            content=request.urlopen(url=url).read().decode('utf-8')

            soup=BeautifulSoup(content,'lxml')

            name_content=str(soup.select('meta[property="og:description"]'))
            # 'meta[property="og:description"]'            name_str=Conduct(name_content)
            name_str = Conduct(name_content)
            print('*'*45+'事迹'+'*'*45)
            for i in range(len(name_str)):
                if (i+1)%60==0:
                    print('\n')
                print(name_str[i],end='')
            print('\n'+'-'*92)

            SJ_name=soup.select('div.anchor-list')
            SJ=soup.select('div.para')
            SJ=Conduct(str(SJ))[len(name_str)+1:]

            print('*'*45+'详细事迹'+'*'*45)
            for i in range(len(SJ)):
                if (i+1)%60==0:
                    print('\n')
                print(SJ[i],end='')
            print('\n')
            print('*'*94)
search()
# ID_1=str(soup.select('a.image-link')[0])
# ID_1=ID_1[ID_1.find('pic')+5+len(name[name.find('=')+1:]):]
# ID_1=ID_1[:ID_1.find('/')]

# 获取ID

# 'https://baikevideo.cdn.bcebos.com/media/mda-XUn7czOmPXU0VoI4/506711985034c2e03c743bc42666ccfb.mp4'

# 'https://baike.baidu.com/api/wikisecond/lemmasecond?lemmaId=30564'
# 通过这个网页上的内容可以看到一个相关视频的下载链接


# url = 'https://baike.baidu.com/api/wikisecond/lemmasecond?lemmaId=' + ID_1
# content_1 = request.urlopen(url=url).read().decode('utf-8')
# content_1=json.loads(content_1)
# url_href=content_1['list']['同词条'][0]['playMp4Url']
# print('正在下载相关视频...')
# Time_1()
# request.urlretrieve(url_href,filename='.\{}.mp4'.format(names))  #下载相关视频
# print('{}.mp4下载成功！'.format(names))


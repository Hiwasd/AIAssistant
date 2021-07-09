#! -*- coding:utf-8 -*-
# _author_: MXM

import time
import requests
import json
import os
from bs4 import BeautifulSoup


def processbar(total, present):
    pass
    time.sleep(0.2)
    percent = int((present/total)*100)
    # {\r} {100} {%} {[} {###} {]}
    if present == total:
        print('{:}{:}{:}{:>6}{}{}'.format('\r','100', '%', '[', '#'*100, ']'), end='\n', flush=True)
    else:
        print('{:}{:}{:}{:>6}{}{}'.format('\r', str(percent), '%', '[', '#' * percent, ']'), end='', flush=True)


# 获取城市代码，获取失败返回false，否则返回城市代码
def get_citycode(city_name):
    # pass
    # 判断城市代码数据是否存在
    if os.path.isfile("citycode"):
        file_read = open("citycode", 'r', encoding="utf-8")
        city_dict = json.load(file_read)
        file_read.close()
        for k,v in city_dict.items():
            if k == city_name:
                return v
        print("can not find city: %s ..."%city_name)
        return False
    else:
        print("can not load citycode file ...")
        return False

# 整合网页链接，返回地区对应的网页链接
def merge_url(city_code):
    # 连接格式为："http://www.weather.com.cn/weather/101020100.shtml"
    url = "http://www.weather.com.cn/weather/%s.shtml"%city_code
    return url

# 解析获取网页链接，获取网页数据，成功则返回requests.content数据
def parse_url(url):
    # 定义请求标头
    headers = {}
    # 用户代理，使得服务器能够识别客户使用的操作系统及版本、CPU 类型、浏览器及版本、浏览器渲染引擎、浏览器语言、浏览器插件等信息
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/91.0.4472.124 \
                    Safari/537.36 \
                    Edg/91.0.864.64"
    headers = {"User-Agent": user_agent}
    # 使用get方法进行访问
    try:
        response = requests.get(url, headers=headers)
        return response.content
    except:
        return False

# 解析地区信息，返回(省份，城市)
def parse_location(location_soup):
    """解析城市地区信息
        :param location_soup: 包含地区信息的beautifulsoup内容块
        :return (province, city): 返回元组
        :retrun False: 解析失败返回False
    """
    # 建立临时列表，存放子节点信息
    location_temp_list = []
    province = ""
    city = ""
    try:
        for child in location_soup.children:
            # 删除空行
            if child.string != '\n':
                location_temp_list.append(child.string)
        province = location_temp_list[2]
        city = location_temp_list[4]
    except:
        return False
    return (province, city)

# 解析天气信息，返回[wea, tem_low, tem_hi, win, win_lev]
def parse_weather(weather_soup):
    """解析天气信息
        :param weather_soup: 包含天气信息的beautifulsoup内容块
        :return [wea, tem_low, tem_hi, win, win_lev]: 解析成功返回列表
        :return False: 解析失败返回False
    """

    # 初始化结果
    wea = ""
    tem_low = ""
    tem_hi = ""
    win = ""
    win_lev = ""
    # 尝试获取wea,tem,win类信息
    try:
        wea_cls = weather_soup.find(class_="wea")
        tem_cls = weather_soup.find(class_="tem")
        win_cls = weather_soup.find(class_="win")
    except:
        return False
    # 获取当日天气
    try:       
        wea = wea_cls.string
    except:
        return False
    # 获取当日温度
    try:
        tem_hi = tem_cls.span.string
    except:
        return False
    try:
        tem_low = tem_cls.i.string[:-1]
    except:
        return False
    # 获取当日风向 
    try:
        win = win_cls.em.span["title"]
    except:
        return False
    try:
        win_lev = win_cls.i.string
    except:
        return False
    # 解析成功则返回结果列表
    return [wea, tem_low, tem_hi, win, win_lev]

if __name__ == "__main__":
    # 初始化变量
    error_code = 0 # 收集函数返回值，生成异常代码
    province = ""
    city = ""
    wea = ""
    tem_low = ""
    tem_hi = ""
    win = ""
    win_lev = ""
    # 初始化变量结束

    city_code = get_citycode("松江")
    if city_code == False:
        error_code += 1
    weather_url = merge_url(city_code)
    content = parse_url(weather_url)
    if content == False:
        error_code += 10
    if error_code == 0:
        # 使用BeautifulSoup解析返回的网页数据
        soup = BeautifulSoup(content, 'lxml')
        # 获取当前城市信息  
        location = soup.find(class_="crumbs fl")
        location_ret = parse_location(location)
        if location_ret == False:
            error_code +=100
        else:
            province,city = location_ret
        # 查找当日的天气信息
        today = soup.find(class_="sky skyid lv3 on")
        wea_ret = parse_weather(today)
        if wea_ret == False:
            error_code +=1000
        else:
            wea, tem_low, tem_hi, win, win_lev = wea_ret
    
    if error_code == 0:
        # 格式化输出
        weather_template = ""
        weather_template = province + city + "，天气" + wea + ", 温度" + tem_low + " " + tem_hi + "摄氏度，" + win + win_lev
        print(weather_template)
    else:
        print("error code ", error_code)
        if (error_code%10 >= 1):
            print("get city code failed ...")
        if (error_code%100 >= 10):
            print("parse url failed ...")
        if (error_code%1000 >= 100):
            print("parse location failed ...")
        if (error_code%10000 >= 1000):
            print("parse weather failed ...")

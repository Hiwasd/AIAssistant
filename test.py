# -*- encoding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

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
response = requests.get("http://www.weather.com.cn/weather/101040300.shtml", headers=headers)
# 使用BeautifulSoup解析返回的网页数据
soup = BeautifulSoup(response.content, 'lxml')

# 获取当前城市信息
location_list = []
location = soup.find(class_="crumbs fl")
for child in location.children:
    if child.string != '\n':
        location_list.append(child.string)
print(location_list)
province = location_list[2]
city = location_list[4]
print(province, city)

# 查找当日的天气信息
today = soup.find_all(class_="sky skyid lv3 on")[0]
# print(today)
# 获取当日天气
wea = today.find(class_="wea").string
print(wea)
# 获取当日温度
tem = today.find(class_="tem")
tem_hi = tem.span.string
print(tem_hi)
tem_low = tem.i.string[:-1]
print(tem_low)
# 获取当日风向
win_cls = today.find(class_="win")
win = win_cls.em.span["title"]
win_lev = win_cls.i.string
print(win)
print(win_lev)

# 格式化输出
weather_template = ""
weather_template = province + city + "地区，天气为" + wea.string + ", " + tem_low + "到" + tem_hi + "摄氏度，" + win + win_lev
print(weather_template)

if __name__ == "__main__":
    pass
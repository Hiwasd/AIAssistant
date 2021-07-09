# 天气网站数据爬取 #
## Python爬虫基本知识 ##  
## Python爬虫代码分析 ##  
### **天气网页分析** ###  
1. 中国天气网主页地址为: http://www.weather.com.cn/  查询天气网页为: http://www.weather.com.cn/weather1d/101020100.shtml 或者 http://www.weather.com.cn/weather/101020100.shtml   
本次选用网页为: http://www.weather.com.cn/weather/101020100.shtml ,页面比较简洁，网页中包含近7天的天气信息，网页为静态网页，可以直接获取数据。其中 101020100 为城市代码，细分到市级，不同城市只需要将对应城市代码替换到网址中，即可访问到对应城市的天气页面。   
2. 
### **爬虫代码分析** ###
**1. main方法**  
1-1. 主要流程  
>查找城市对应的代码编号，对应方法*getget_citycode(city_name)* , 其中城市名称需要为中文;  
>根据城市代码补全网址，对应方法*merge_url(city_code)* ;    
>访问网页，获取网页内容，对应方法*parse_url(url)* ;  
>提取地区信息块，通过*parse_location(location_soup)* 方法进行解析;   
>提取天气信息块，通过*parse_weather(weather_soup)* 方法进行解析;     
>将结果进行格式化 

1-2. 代码说明  
```python
if __name__ == "__main__":
```
这个判断主要针对该文件中的方法被其他文件进行调用时，不执行这个语句之后的内容，但是在单独运行该文件时，会正常执行这个语句之后的内容，方便调试该文件中所定义的类和方法。 

```python
city_code = get_citycode("上海")
if city_code == False:
    error_code += 1
```
调用 *get_citycode()* 方法，获取上海地区对应的城市编码。该方法在获取编码失败时，会返回False，可以通过判断返回值是否为False判断是否成功获取编码，若获取失败，则将error_code错误信息码 +1 。
>其他方法的调用不再展开，详细信息在分析具体方法十介绍。本次示例中的方法返回值都是错误的时候返回False。四个方法每次调用失败，对应error_code的值都会 +1，+10，+100，+1000，用于区分不同方法的调用情况。
```python 
# 使用BeautifulSoup解析返回的网页数据
soup = BeautifulSoup(content, 'lxml')
# 获取当前城市信息  
location = soup.find(class_="crumbs fl")
```
通过 BeautifulSoup 解析网页内容，解析器为'lxml'。根据网页内容分析，网页中的城市信息包含在 "crumbs fl" 中，通过 find（）方法可以查找到对应的内容块。同理可以查找提取出天气信息对应的内容块。
```python
weather_template = province + city + "，天气" + wea + ", 温度" + tem_low + " " + tem_hi + "摄氏度，" + win + win_lev
```
天气结果输出的模板为 XXXX(地区)，天气XXXX，温度XXXX摄氏度，XXXX(风向及风力等级)。采用字符串拼接的方式，可以根据需求进行修改。   
**2. get_citycode(city_name)**  
```python
if os.path.isfile("citycode"):
```
os.path.isfile(path)，判断 path 所指定的是否是一个文件，需要导入 os 模块。该文件以字典的方式保存全国城市对应的城市编码，格式为json格式。  
>tips:   
os模块中常用到的方法  
>1.获取绝对路径：os.path.abspath(path)，os.path.abspath(\_\_file\_\_)返回当前py文件的绝对路径；  
>2.获取目录：os.path.dirname(path)；  
>3.判断路径是否存在，存在返回True，否则返回False：os.path.exists(path)；  
>4.合成路径：os.path.join(path1[, path2[, ...]])   
```python
file_read = open("citycode", 'r', encoding="utf-8")
city_dict = json.load(file_read)
file_read.close()
```
以只读的方式打开当前目录下的 citycode 文件，并解码json数据，返回为pytho中对应的类型。
```python
for k,v in city_dict.items():
    if k == city_name:
        return v
print("can not find city: %s ..."%city_name)
return False
```
遍历字典，如果键等于输入的城市名称，则输出对应的值。如果遍历完整个字典都没有找到对应的键，则返回False。

**3. merge_url(city_code)**  
```python
url = "http://www.weather.com.cn/weather/%s.shtml"%city_code
return url
```
生成网页链接，通过 %s 占位符，空出字符串中的位置，并将获取到的城市编码替换进去。格式为"http://www.weather.com.cn/weather/101020100.shtml"。   
**4. parse_url(url)** 
```python
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/91.0.4472.124 \
                Safari/537.36 \
                Edg/91.0.864.64"
headers = {"User-Agent": user_agent} 
``` 
用户代理，使得服务器能够识别客户使用的操作系统及版本、CPU 类型、浏览器及版本、浏览器渲染引擎、浏览器语言、浏览器插件等信息。不同的网站要求不一样，本次访问的天气网没有要求必须要填写用户代理数据。  
```python
response = requests.get(url, headers=headers)
```
以get方式，访问页面。   
**5. parse_location(location_soup)**  
```python
for child in location_soup.children:
    # 删除空行
    if child.string != '\n':
        location_temp_list.append(child.string)
province = location_temp_list[2]
city = location_temp_list[4]
```
```html
<!--网页中对应的数据 -->
<div class="crumbs fl">
    <a href="http://www.weather.com.cn/forecast/" target="_blank">全国</a>
    <span>&gt;</span>
    <a>上海</a>
    <span>&gt;</span>
    <span>城区</span>
</div>
```
根据网页中的源码数据，可以看出在地区的数据中，包含若干个子节点，可以通过遍历子节点的方式获取信息，并将内容添加到列表中，列表的格式为 ['全国','>','上海','>','城区'](删除空行后)，所以我们所需要的元素在第2个和第4个。   
**6. parse_weather(weather_soup)**  
```python
wea_cls = weather_soup.find(class_="wea")
tem_cls = weather_soup.find(class_="tem")
win_cls = weather_soup.find(class_="win")
```
分析方法同上。




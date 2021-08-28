import os
import re
import requests
import time
from pathlib import Path as P


def get_one_page(url):  # 解析给定url的网页源代码
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    response = requests.get(url, headers=headers)
    time.sleep(5)
    if(response.status_code == 200):  # 状态码200说明返回状态正确，状态码是404,403等其他代号则说明网页请求失败
        return response.text
    return None


def download(url, filename):  # 下载图片到本地文件夹
    file_path = P.cwd() 
    filepath = str(file_path) + '/' + str(filename) + '.jpg'  # 这里的路径可以更改自己的文件夹
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    if os.path.exists(filepath):  # 判断图片路径是否已经存在，如果存在就不保存了
        return
    with open(filepath, 'wb')as f:  # 把图片以二进制形式写入到本地
        response = requests.get(url, headers=headers)
        f.write(response.content)


def parse(html):  # 解析网页源代码
    pattern = re.compile(
        'data-progressive="(.*?)".*?<h3>(.*?)</h3>')  # 正则表达式筛选html
    items = re.findall(pattern, html)
    for item in items:
        try:
            url = item[0].replace('640', '1920').replace(
                '480', '1080')  # 替换图片尺寸
            # print(url)
            imagename = item[1].strip()
            rule = re.compile(r'[a-zA-z1-9()-/]')  # []用来表示一组字符【abc】匹配a,b,或c
            imagename = rule.sub('', imagename)
            download(url, imagename.strip())
            print(imagename, "正在下载")
        except Exception:
            continue


if __name__ == '__main__':
    for page in range(1, 40):  # 爬取页面的范围，可以随意更改
        url = 'https://bing.ioliu.cn/?p='+str(page)
        print("正在抓取第", page, "页", url)
        html = get_one_page(url)
        parse(html)
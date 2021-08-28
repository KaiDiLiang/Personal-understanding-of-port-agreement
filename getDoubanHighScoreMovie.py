# 可解决中文乱码
from __future__ import unicode_literals
# -*- coding:utf-8 -*-
import json
from json import encoder
from os import sep
import requests
import random
import csv
import pymysql
import pandas as Pd
import time
from pathlib import Path as Pa
from requests.api import head
from sqlalchemy import create_engine, engine,Table,MetaData
from sqlalchemy.orm import Session

def getTags(p_id):
  tags = []
  header_list = [ 
    {
      "Accept": "*/*",
      
      "Accept-Language": "zh-CN,zh;q=0.9",
     
      "sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="91", " TencentTraveler";v="91"',
      "sec-ch-ua-mobile": "?0",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-origin",      
      "Referer": "https://movie.douban.com/explore",
      "Host": "movie.douban.com",
      "user-agent": "User-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)"
    },
    {
      "Accept": "*/*",
      
      "Accept-Language": "zh-CN,zh;q=0.9",
     
      "sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="91", " Firefox";v="91"',
      "sec-ch-ua-mobile": "?0",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-origin",
      "Referer": "https://movie.douban.com/explore",
      "Host": "movie.douban.com",
      "user-agent": "User-Agent:Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1"
    },
    {
      "Accept": "*/*",
      
      "Accept-Language": "zh-CN,zh;q=0.9",
     
      "sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="91", " safari";v="91"',
      "sec-ch-ua-mobile": "?0",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-origin",
      "Referer": "https://movie.douban.com/explore",
      "Host": "movie.douban.com",
      "user-agent": "User-Agent:Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"
    },
    {
      "Accept": "*/*",
      
      "Accept-Language": "zh-CN,zh;q=0.9",
     
      "sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="91", "Opera";v="91"',
      "sec-ch-ua-mobile": "?0",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-origin",
      "Referer": "https://movie.douban.com/explore",
      "Host": "movie.douban.com",
      "user-agent": "User-Agent:Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11"
    },
    {
      "Accept": "*/*",
      
      "Accept-Language": "zh-CN,zh;q=0.9",
     
      "sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="91", "Microsoft Edge";v="91"',
      "sec-ch-ua-mobile": "?0",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-origin",
      "Referer": "https://movie.douban.com/explore",
      "Host": "movie.douban.com",
      "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66"
    },
    {
      "Accept": "*/*",
      
      "Accept-Language": "zh-CN,zh;q=0.9",
     
      "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="91", "Google Chrome";v="91"',
      "sec-ch-ua-mobile": "?0",
      "Sec-Fetch-Dest": "empty",
      "Sec-Fetch-Mode": "cors",
      "Sec-Fetch-Site": "same-origin",
      "Referer": "https://movie.douban.com/explore",
      "Host": "movie.douban.com",
      "user-agent": "Mozilla/5.0(Windows NT 10.0; Win64; x64)AppleWebKit/537.36(KHTML, like Gecko)Chrome/90.0.4430.212 Safari/537.36"
    }
  ]
  parmas = {
    'type': 'movie',
    'tag': '豆瓣高分',
    'sort': 'recommend',
  }
  id = p_id
  url = 'https://movie.douban.com/j/search_subjects?type='+parmas['type']+'&tag='+ parmas['tag']+'&sort='+parmas['sort']+'&page_limit=20'+'&page_start={}'.format(id)
  print(url)
  req = requests.get(url, headers=header_list[random.randint(0,5)]).json()
  '''
    # 写入json格式文件
    with open('./douban.text', 'w+', encoding='utf-8') as f:
    f.write(json.dumps(req, ensure_ascii=False, indent=2))
  '''
  # 提前预览列名，当下面代码写入数据时，会将其一一对应
  # 列名跟数据必须一致
  line_header = [
    'rate', 'title', 'url', 'cover', 'id',
    'is_new','cover_x', 'cover_y', 'playable', 'episodes_info'
  ]
  # w+读写并删旧有内容，a+读写并追加内容
  with open('./douban.csv', 'a+', encoding='utf-8',newline='') as f:
    csv_W = csv.DictWriter(f,fieldnames=line_header)
    csv_W.writeheader()
    csv_W.writerows(req['subjects'])
  time.sleep(random.randint(5,10))

def clean_data():
  # 取出douban.csv中的电影数据
  file = open('./douban.csv',encoding='utf-8')
  read_csv = Pd.read_csv(file, encoding='utf-8', header=None)
  read_csv_list = read_csv.drop_duplicates()
  read_csv_list.to_csv('./douban.csv', index=False,header=False)

def connMysql():
  config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '012346',
    'charset': 'utf8mb4',
    'local_infile': 1,
    'database': 'doubanhightscoremovie_db'
  }
  # 链接数据库
  conn = pymysql.connect(**config)
  # 用cursor()方法创建游标对象cursor
  cur = conn.cursor()
  '''
    pandas的head()方法读取数据
    print(read_csv.head(),read_csv.shape[0])
  '''
  # 取出douban.csv中的电影数据
  file = open('./douban.csv',encoding='utf-8')
  read_csv_file = Pd.read_csv(file, encoding='utf-8', header=None)
  # 6小时更新一次数据，清除数据表的旧数据，以免旧有数据污染新数据
  cur.execute("truncate table doubanhightscoremovie_url_tb;")
  conn.commit()
  '''
    将DataFrame的数据储存到数据库表中，如果库里没有该表名，则会自动创建该表
    if_exits： 三个模式：fail，若表存在，则不输出；replace：若表存在，覆盖原来表里的数据；append：若表存在，将数据写到原表的后面。默认为fail
    index：是否将df的index单独写到一列中
    chunksize：设置一次入库的大小
  engine = create_engine('mysql+pymysql://root:012346@localhost:3306/doubanhightscoremovie_db', echo= True)
  r_csv = Pd.read_csv(file)
  r_csv.to_sql('doubanhightscoremovie_url_tb', engine, if_exists='append',index=False,chunksize=1000)
  '''
  # pymysql原生操作
  for i in range(read_csv_file.shape[0]):
    # 用pandas的iloc()或loc()切片行数据
    loc_data = read_csv_file.loc[i]
    loc_data['episodes_info'] = ' '
    clean_data = loc_data
    # clean_data = (loc_data['rate'], loc_data['title'], loc_data['url'],loc_data['cover'],loc_data['id'], loc_data['is_new'], loc_data['cover_x'], loc_data['cover_y'],loc_data['playable'], loc_data['episodes_info'])
    # print(i,loc_data,)
    try:
      sql = "insert into doubanhightscoremovie_url_tb(rate,title,url,cover,m_id,is_new,cover_x,cover_y,playable,episodes_info) values " + str(clean_data) + ";"
      cur.execute(sql)
      conn.commit()
    except:
      # 如果发生错误则回滚
      conn.rollback()
      print('数据库操作失败！')

  # # 关闭数据库链接
  conn.close()

if __name__ == '__main__':
  # 清除旧有文件，便于几份数据合并，清理旧有数据
  file_path = Pa('./douban.csv')
  # if file_path.is_file():
  #   file_path.unlink()
  # else:
  #   pass
  # p_id = [0, 20, 40, 60, 80]
  # for i in p_id:
  #   getTags(i)
  # clean_data()
  connMysql()
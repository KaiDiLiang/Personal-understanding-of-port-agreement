from json import encoder
import requests
from lxml import etree
import time
import random
import json
import re
from pathlib import Path as P
import _thread


class Spider():
	def __init__(self):
		self.headers = {
				"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
				"accept-encoding": "gzip, deflate, br",
				"accept-language": "zh-CN,zh;q=0.9",
				"cache-control": "max-age=0",
				"if-none-match": 'W/"607e3045-24d8"',
				"sec-ch-ua": '"Not A;Brand";v="99", "Chromium";v="90", "Microsoft Edge";v="90"',
				"sec-ch-ua-mobile": "?0",
				"sec-fetch-dest": "document",
				"sec-fetch-mode": "navigate",
				"sec-fetch-site": "none",
				"sec-fetch-user": "?1",
				"upgrade-insecure-requests": "1",
				"referer": "https://m.meitu131.net/",
				"authority": "m.meitu131.net",
				"method": "GET",
				"scheme": "https",
				"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 Edg/90.0.818.66"
		}
		self.file_path = P.cwd()
		self.base_url = "https://m.meitu131.net/meinv/"

	def test(self, url_number):
		data_url = []
		for i in range(1, 80):
			if i == 1:
					url = self.base_url + str(url_number) + "/index.html"
			else:
					url = self.base_url + str(url_number) + "/index_" + \
							str(i) + ".html"
			data_url.append(url)
		for i in range(79):
			res = requests.get(data_url[i], headers=self.headers)
			print('正在爬取第' + str(i) + '张')
			etree_res = etree.HTML(res.text, etree.HTMLParser())
			time.sleep(2)
			xpath_res_alt = etree_res.xpath('//p/a/img/@alt')
			xpath_res_src = etree_res.xpath('//p/a/img/@src')
			d_file = requests.get((xpath_res_src[0]), headers=self.headers)
			if P('./' + xpath_res_alt[0]).is_dir():
					None
			else:
					P(self.file_path/xpath_res_alt[0]
						).mkdir(parents=True, exist_ok=True)
			with open('./' + xpath_res_alt[0] + '/' + xpath_res_alt[0] + str(i) + '.jpg', 'wb+') as jpg_file:
					jpg_file.write(d_file.content)
					jpg_file.close()
			time.sleep(random.randint(5, 10))
		print('完成！@_@')

	def blazers(self):
		base_url = 'https://m.meitu131.net/nvshen/4/'
		res_data = requests.get(base_url, headers=self.headers)
		etree_data = etree.HTML(res_data.text, etree.HTMLParser())
		base_data = {}
		etree_alt_data = []
		etree_src_data = []
		etree_alt = etree_alt_data.append(etree_data.xpath(
		    '//div[@class="am-gallery-item"]/a/img/@alt'))
		etree_src = etree_src_data.append(
		    (etree_data.xpath('//div[@class="am-gallery-item"]/a/@href')))
		print(etree_data.xpath('//div[@class="am-gallery-item"]/a/@href'))
		# re.compile(r'\d+')
		# print(etree_src_data)
		quit()
		for i in zip(etree_alt_data, etree_src_data):
			base_data = {etree_alt[i], etree_src[i]}
		print(base_data)
		return base_data
		with open('./json_data.txt', 'w+', encoding='utf-8') as json_text:
			json_text.write(res_data.text)
			json_text.close()

	def join_url(self, base_data):
		print(base_data)


if __name__ == '__main__':
	the_spider = Spider()
	# count_1 = 0
	# while count_1 < 9:
	# 	try:
	# 		_thread.start_new_thread( the_spider.test() )
	# 		_thread.start_new_thread( the_spider.test() )
	# 		_thread.start_new_thread( the_spider.test() )
	# 		_thread.start_new_thread( the_spider.test() )
	# 	except:
	# 		print('多线程失败')
	the_spider.test(5090)
	# the_spider.blazers()

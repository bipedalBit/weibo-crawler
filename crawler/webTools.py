#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
脚本描述: webTools模块中是其他模块经常使用的一些工具函数。
author: Bipedal Bit
email: me@bipedalbit.net
'''

from bs4 import BeautifulSoup # 引入XML字符串操作类的对象生成方法
from urllib2 import Request # 引入基础HTTP通信包的HTTP请求生成方法

def tag_to_soup(tag):
	'''
	将BeautifulSoup查询得到的tag对象转换为新的可查询的BeautifualSoup对象。
	'''
	return BeautifulSoup(str(tag), 'lxml')

def get_request(url, data = None, cookie = None, referer = None):
	'''
	按特定参数获取HTTP请求对象，data为可选项（post请求需要设定data参数），cookie为可选项，referer为可选项。
	生成的请求对象模拟的是Ubuntu下火狐浏览器的行为。
	'''
	headers = {
		'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:42.0) Gecko/20100101 Firefox/42.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
		'DNT': '1',
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0'
	}
	if cookie is not None: headers['cookie'] = cookie
	if referer is not None: headers['Referer'] = referer
	request = Request(
		url = url,
		headers = headers,
		data = data
	)
	return request
#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
脚本描述: crawler模块中定义了网络爬虫的相关函数。
author: Bipedal Bit
email: me@bipedalbit.net
'''

from time import sleep # 引入休眠方法
from random import random # 引入取随机数方法
import re # 引入正则表达式模块
import MySQLdb # MySQL数据库相关操作包
import urllib2 # 基础HTTP通信包
from webTools import get_request # 引入自定义web工具模块的get_request函数

# 网络爬虫使用的默认cookie
cookie = ''
# 网络爬虫所需的登录用户名
username = ''
# 网络爬虫所需的登录密码
password = ''
# 数据库名
dbname = 'crawl_result'
# 存放爬取数据的数据表名
tablename = 'weibo'
# 数据库用户名
dbuser = 'root'
# 数据库密码
dbpwd = 'root'
# 数据库地址
dbhost = 'localhost'
# 数据库端口
dbport = 3306

def log_raw_result(raw_result):
	'''
	记录当前请求返回的生数据
	'''
	f = open('raw_result.htm', 'w')
	f.write(raw_result)
	f.close()

def clear_log():
	'''
	清空爬虫日志文件
	'''
	f = open('log', 'w')
	f.close()

def crawl(url, parser, login, group_len, average_delay, page_limit = None, record_raw_data = False):
	'''
	在指定url用指定登录器和解析方法爬取页面数据并保存，返回爬取数据数，爬取页面上限为可选项。
	url: 爬虫起点地址
	parser: 页面解析器函数
	login: 登录器函数
	group_len: 每组连续请求的请求数
	average_delay: 每组请求的平均延时，实际延时将是平均延迟周围的一个随机值
	page_limit: 爬取页面上限，可选项
	record_raw_data: 是否记录页面生数据，默认不记录
	'''
	# 引入模块的全局变量
	global cookie
	global username
	global password
	# 获取request对象
	request = get_request(url, cookie)
	# 记录爬取的页数
	p = 1
	# 记录爬取的数据数
	data_cnt = 0
	clear_log() # 清空爬虫日志
	f = open('log', 'a') # 打开爬虫日志
	while True:
		request = get_request(url, cookie)
		response = urllib2.urlopen(request)
		raw_result = response.read()
		if raw_result is None: continue # 如果请求未返回，立即重试
		actual_url = response.geturl() # 获取实际访问页面地址
		if actual_url != url: # 被服务器执行了请求重定向
			if re.search('login', actual_url) is not None:
				print 'cookie无效或已经过期失效，重新登录'
				cookie = login(username, password)
			else:
				print '账号的访问请求被服务器重定向，IP可能被封禁，等待30秒'
				sleep(30)
			continue # 重新尝试爬取该页
		if record_raw_data: log_raw_result(raw_result) # 记录当前请求返回的生数据
		page_result = None
		try: page_result = parser(url, request.get_host(), raw_result) # 尝试解析页面
		except: # 如果页面解析不成功，可能页面结构已经发生变化，停止爬虫
			print '页面解析失败，停止爬虫'
			break
		f.write('从"' + url + '"爬取' + str(len(page_result['data_list'])) + '条数据\n') # 记录爬虫日志
		# 保存熟数据（SQL录入）
		if len(page_result['data_list']) > 0: write_DB(data_list = page_result['data_list'])
		p += 1 # 页面数加1
		data_cnt += len(page_result['data_list']) # 更新解析出的数据数
		# 检查是否到达指定的爬取页面上限
		if page_limit is not None and p > page_limit: break
		# 检查是否已经没有下一页
		if page_result['next_page_link'] is None: break
		# 更新目标url
		else: url = page_result['next_page_link']
		if p % group_len == 0:  # 每爬取一组页面延时下一次请求，防止连续频繁请求丢数据
			delay = random()*(2*average_delay - 2) + 1 # 计算一个以1为下限以average_delay为平均值的随机延迟
			sleep(delay) # 执行延迟
	f.close() # 关闭爬虫日志
	return data_cnt

def write_DB(data_list):
	'''
	保存熟数据，将爬虫获得的格式化数据录入MySQL数据库。
	'''
	# 引入模块的全局变量
	global dbhost
	global dbport
	global dbuser
	global dbpwd
	global dbname
	global tablename
	conn = MySQLdb.connect(
		host = dbhost,
		port = dbport,
		user = dbuser,
		passwd = dbpwd,
		db = dbname,
		charset = 'utf8'
	)
	cur = conn.cursor()
	for data in data_list:
		placeholders = []
		for value in data.values(): placeholders.append('%d' if type(value) is int else '\'%s\'')
		sql = 'insert into `' + tablename + '`(`' + '`,`'.join(data.keys()) + '`) values(' + ','.join(placeholders) + ')'
		# 微博ID重复则跳过，避免数据重复
		try: cur.execute(sql % tuple(data.values()))
		except: continue
	cur.close()
	conn.commit()
	conn.close()
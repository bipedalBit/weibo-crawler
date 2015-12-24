#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
包描述: crawler包最初只是我为了爬取新浪微博中某个用户使用特定客户端发送的微博数据而编写的一个工具脚本。
实现需要的功能后，我又为脚本添加了一些功能，尤其是新浪微博的模拟登录功能。
然后对爬虫的各个过程进行了模块化封装，把脚本扩展成了包。
脚本描述: __init__.py脚本可以看作是crawler包的索引脚本，负责将包内所有模块组织起来。
author: Bipedal Bit
email: me@bipedalbit.net
'''

import sys # 引入系统包
import weiboParser # 引入一个页面解析器模块
import weiboLogin # 引入登录模块
import crawler # 引入爬虫模块
from time import time # 引入取当前时间戳方法

def get_time_cost_str(time_cost):
	'''
	格式化时间开销（time()函数返回值的差），返回时间开销字符串。
	'''
	int_time_cost = int(time_cost)
	time_cost_str = ''
	day_seconds = 3600*24
	if time_cost < 60:
		time_cost_str += str(time_cost) + '秒'
	elif 60 <= time_cost < 3600:
		time_cost_str += str(int_time_cost/60) + '分' + str(time_cost%60) + '秒'
	elif 3600 <= time_cost < day_seconds:
		time_cost_str += str(int_time_cost/3600)  + '小时' + str(int_time_cost/60%60) + '分' + str(time_cost%60) + '秒'
	else:
		time_cost_str += str(int_time_cost/day_seconds) + '天' + str(int_time_cost/3600%24)  + '小时'\
		+ str(int_time_cost/60%60) + '分' + str(time_cost%60) + '秒'
	return time_cost_str

def main():
	'''
	定义一个入口函数来组织爬虫过程，虽然对于python来说入口函数的形式并不必要.
	'''
	# 指定系统默认编码为utf-8
	default_encoding = 'utf-8'
	if sys.getdefaultencoding() != default_encoding:
		reload(sys)
		sys.setdefaultencoding(default_encoding)

	# 执行爬虫过程
	url = 'http://weibo.cn/moegirlwiki' # 任意新浪微博移动版页面地址
	# username = 'Your weibo username' # 新浪通行证用户名
	# password = 'Your weibo password' # 新浪通行证密码
	crawler.username = raw_input('请输入新浪通行证用户名：')
	crawler.password = raw_input('请输入新浪通行证密码：')

	time0 = time()
	weibo_cnt = crawler.crawl(
		url = url,
		parser = weiboParser.wap_weibo_parser,
		login = weiboLogin.wap_login,
		group_len = 1,
		average_delay = 3,
		page_limit = 1000,
		# record_raw_data = True
	)
	time_cost = time() - time0
	print '共爬取数据', weibo_cnt, '条，用时' + get_time_cost_str(time_cost)
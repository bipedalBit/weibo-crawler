#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
脚本描述: weiboParser模块中定义了新浪微博页面的解析过程相关的函数。
author: Bipedal Bit
email: me@bipedalbit.net
'''

from bs4 import BeautifulSoup # 引入XML字符串操作类的对象生成方法
from webTools import tag_to_soup # 引入自定义web工具模块的tag_to_soup函数
import re # 引入正则表达式模块
from datetime import datetime, timedelta # 引入日期与时间类、时间差类

def wap_weibo_data_parser(data_list, weibo_soup, client_info_soup):
	'''
	用于新浪微博移动版用户主页每个的微博标签的数据解析。
	可能解析出的数据项包括：
	weibo_id: 微博唯一标识字符串
	datetime: 微博时间
	client: 微博客户端
	content: 微博原文
	image_url: 微博图片地址
	attitude_cnt: 微博点赞数
	repost_cnt: 微博转发数
	comment_cnt: 微博评论数
	comment_url: 微博评论地址
	repost_flag: 微博转发标识
	org_weibo_user: 微博原文作者
	org_weibo_user_url: 微博原文作者主页地址
	'''
	data = {}
	# 获取微博ID
	data['weibo_id'] = weibo_soup.div['id']
	# 获取客户端信息，即时间和客户端类型
	client_info = ''.join(client_info_soup.strings).split(u'\xa0来自')
	# 获取日期、时间
	datetime_ = client_info[0].encode('utf8').split(' ')
	# 获取当前日期、时间
	now = datetime.now()
	# 时间格式为DD分钟前
	if len(datetime_) == 1:
		minutes_delta = int(datetime_[0].split('分钟前')[0])
		dt = (now - timedelta(minutes = minutes_delta))
		data['datetime'] = str(dt.date()) + ' ' + dt.strftime('%I:%M')
	# 时间格式为今天 HH:MM
	elif len(datetime_) == 2 and datetime_[0] == '今天':
		data['datetime'] = str(now.date()) + ' ' + datetime_[1]
	# 时间格式为MM月DD日 HH:MM
	elif datetime_[0].find('月') != -1:
		month = int(datetime_[0].split('月')[0])
		day = int(datetime_[0].split('月')[1].split('日')[0])
		dt = datetime(now.year, month, day)
		data['datetime'] = str(dt.date()) + ' ' + datetime_[1]
	# 时间格式为YY-MM-DD HH:MM
	else:
		data['datetime'] = client_info[0]
	# 获取客户端类型
	data['client'] = client_info[1].encode('utf8')
	# 获取微博正文
	data['content'] = ''.join(tag_to_soup(weibo_soup.find('span', class_ = 'ctt')).strings).encode('utf8')
	# 获取图片链接
	if weibo_soup.find('img', class_ = 'ib') is not None:
		image_soup = tag_to_soup(weibo_soup.find('img', class_ = 'ib').parent)
		data['image_url'] = image_soup.a['href']
	# 获取微博中的所有div子标签
	div_list = weibo_soup.find_all('div', class_ = False)
	# 获取赞数
	attitude_soup = tag_to_soup(tag_to_soup(div_list[-1]).find('a', href = re.compile('^http://weibo.cn/attitude/')))
	data['attitude_cnt'] = int(re.search(r'\d+', attitude_soup.string).group(0))
	# 获取转发数
	repost_soup = tag_to_soup(tag_to_soup(div_list[-1]).find('a', href = re.compile('^http://weibo.cn/repost/')))
	data['repost_cnt'] = int(re.search(r'\d+', repost_soup.string).group(0))
	# 获取评论数
	comment_soup = tag_to_soup(tag_to_soup(div_list[-1]).find('a', class_ = 'cc'))
	data['comment_cnt'] = int(re.search(r'\d+', comment_soup.string).group(0))
	# 获取评论地址
	data['comment_url'] = comment_soup.a['href']
	# 如果微博为转发型
	if weibo_soup.find('span', class_ = 'cmt') is not None:
		# 标记为转发型微博
		data['repost_flag'] = 1
		post_user_soup = tag_to_soup(tag_to_soup(div_list[0]).span.a)
		data['org_weibo_user'] = post_user_soup.a.string
		data['org_weibo_user_url'] = post_user_soup.a['href']
		# 获取微博最后一个div标签的第二段文本内容为转发理由
		str_generator = tag_to_soup(div_list[-1]).strings
		str_generator.next() # 跳过第一段文本即“转发理由:”
		data['repost_reason'] = str_generator.next()
	# 如果微博为原创型
	else: data['repost_flag'] = 0 # 标记为非转发型微博
	data_list.append(data)

def wap_weibo_parser(url, host, data):
	'''
	用于新浪微博移动版用户主页的微博数据解析。
	按特定url、host地址和特定页面生数据（刚获取的HTML字符串）解析页面数据，
	获取页面微博内容数据weibo_list数组和页面跳转链接next_page_link。
	'''
	# 获取页面BueatifulSoup对象
	soup = BeautifulSoup(data, 'lxml')
	# 获取各条微博的Tag对象
	weibo_list = soup.find_all('div', class_ = 'c', id = re.compile(''))
	# 获取下一页链接
	next_page_link = re.search('(?<=href=").+(?=">下页)', str(soup.find('div', id = 'pagelist')))
	data_list = []
	# 提取目标主页的用户微博ID
	user_tag_soup = tag_to_soup(soup.find('div', class_ = 'ut'))
	weibo_user = user_tag_soup.strings.next().encode('utf8')
	# 当前页不是是微博主页首页
	if user_tag_soup.find('span', class_ = 'ctt') is None:
		weibo_user = re.search('.+(?=的微博)', weibo_user).group(0)
	# 遍历当前页面的微博，解析数据
	for weibo in weibo_list:
		# 获取微博的BueatifulSoup对象
		weibo_soup = tag_to_soup(weibo)
		# 获取微博客户端标签的BueatifulSoup对象
		client_info_soup = tag_to_soup(weibo_soup.find('span', class_ = 'ct'))
		# 微博过滤器，是否解析当前微博的数据
		weibo_filter = True
		# 私货：根据客户端类型过滤来自萌百自动机的微博
		weibo_filter = client_info_soup.find(text = re.compile(u'来自萌娘百科')) is None
		if weibo_filter:
			# 解析微博细节数据
			wap_weibo_data_parser(data_list, weibo_soup, client_info_soup)
			# 添加目标用户的微博ID和主页链接
			data_list[-1]['weibo_user'] = weibo_user
			data_list[-1]['weibo_user_url'] = url
	if next_page_link is not None: next_page_link = 'http://' + host + str(next_page_link.group(0)) + '/'
	page_result = {
		'data_list': data_list,
		'next_page_link': next_page_link
	}
	return page_result
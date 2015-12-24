#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
脚本描述: weiboLogin模块中定义了新浪微博模拟登录过程相关的函数及类。
author: Bipedal Bit
email: me@bipedalbit.net
'''

import urllib2 # 引入基础HTTP通信包
import re # 引入正则表达式模块
from bs4 import BeautifulSoup # 引入XML字符串操作类的对象生成方法
import urllib # 引入原版基础HTTP通信包
import webTools # 引入自定义web工具模块

class MyRedirectHandler(urllib2.HTTPRedirectHandler):
	'''
	继承urllib2.HTTPRedirectHandler类，封装http_error_302方法。
	在自动执行重定向发送新的HTTP请求前提取附在请求头中的cookie，
	提取cookie中模拟登录必需的字段并存储在类成员变量中。
	'''
	# 类成员变量，存储以登录状态访问新浪微博必需的cookie字段
	cookie = ''

	def http_error_302(self, req, fp, code, msg, headers):
		'''
		添加cookie处理过程，然后调用原http_error_302方法执行自动跳转。
		'''
		cookie = str(headers["Set-Cookie"])
		if re.search('SUB=.+?;', cookie) is not None:
			MyRedirectHandler.cookie = re.search('SUB=.+?(?=;)', cookie).group(0)
		req.add_header("Cookie", cookie)
		return urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)

def get_post_needs():
	'''
	从新浪微博移动版登录页面获得登录post请求的必要数据：
	url: 登录页面url，将作为登录post请求头的Referer字段
	action_url: 登录post请求的目标地址
	password_name: 登录post请求中密码数据的数据名
	vk: 登录post请求中vk数据的值
	'''
	url = 'http://login.weibo.cn/login/?ns=1&revalid=2&backURL=http://weibo.cn/&backTitle=微博&vt='
	referer = 'http://weibo.cn/pub/?vt='
	request = webTools.get_request(url = url, referer = referer)
	text = urllib2.urlopen(request).read()
	soup = BeautifulSoup(text, 'lxml')
	action_url = 'http://login.weibo.cn/login/' + soup.form['action']
	password_tag = soup.find('input', type = 'password')
	password_name = re.search('(?<=name=")\w+(?=")', str(password_tag)).group(0)
	vk_tag = soup.find('input', attrs = {'name': 'vk'})
	vk = re.search('(?<=value=")\w+(?=")', str(vk_tag)).group(0)
	return url, action_url, password_name, vk

def get_form_data(username, password, password_name, vk):
	'''
	使用从新浪微博移动版登录页面获取的参数和已知的固定参数填充表单，
	生成表单数据字符串。
	'''
	form_data = {
		'mobile': username,
		password_name: password,
		'remeber': 'on',
		'backURL': 'http://weibo.cn/',
		'backTitle': '微博',
		'tryCount': '',
		'vk': vk,
		'submit': '登录'
	}
	form_data = urllib.urlencode(form_data)
	return form_data

def wap_login(username, password):
	'''
	按照新浪通信证的用户名和密码进行新浪微博移动版的模拟登录，
	获取以登录状态访问新浪微博移动版页面必需的cookie字段。
	'''
	referer, url, password_name, vk = get_post_needs()
	data = get_form_data(username, password, password_name, vk)
	opener = urllib2.build_opener(MyRedirectHandler)
	response = opener.open(webTools.get_request(url = url, data = data, referer = referer))
	# 以下３行判定可以省略，保险起见保留源码
	# text = response.read()
	# redirected_url = re.search(r'(?<=replace\(").+?(?=")', text).group(0)
	# urllib2.urlopen(get_request(url = redirected_url, referer = url))
	return MyRedirectHandler.cookie

# 以下是模拟登录测试代码
if __name__ == '__main__':
	import sys # 引入系统包

	default_encoding = 'utf-8'
	if sys.getdefaultencoding() != default_encoding:
		reload(sys)
		sys.setdefaultencoding(default_encoding)

	username = raw_input('请输入新浪通行证用户名：')
	password = raw_input('请输入新浪通行证密码：')
	url = 'http://weibo.cn/moegirlwiki' # 任意新浪微博移动版页面地址

	cookie = wap_login(username, password)
	request = webTools.get_request(url = url, cookie = cookie)
	opener = urllib2.build_opener(urllib2.HTTPHandler)
	response = opener.open(request)
	if response.geturl() != url: print '登录失败！'
	else: print '登录成功！'
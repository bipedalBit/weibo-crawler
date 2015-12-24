# crawler
&nbsp;&nbsp;&nbsp; Generally, this is a python tool package for network crawling.Though at the very beginning I just wrote a single python script to get some specified weibo data from [weibo.cn](http://weibo.cn/) soon I decided to expand it into a more reusable package.
&nbsp;&nbsp;&nbsp; It's my first time using python to implement a real tool which can fit my needs. In other words, I'm new in programming with python. So the package may looks strange somehow.
&nbsp;&nbsp;&nbsp; The package has 4 modules:
- crawler: Functions about crawling web pages start with a specified url.
- weiboParser: Functions about parsing an individual page to get weibo data items.
- weiboLogin: Functions and classes about login procedure of weibo.([weibo.cn](http://weibo.cn/) only for now)
- webTools: Several tool functions such as encapsulation of urllib2.Request and bs4.BueatifulSoup.

### Depends
&nbsp;&nbsp;&nbsp; This package have only 2 dependent packages which are Python-bs4 and Python-lxml.
&nbsp;&nbsp;&nbsp; You can install them by following commands under Ubuntu:
&nbsp;&nbsp;&nbsp; `sudo apt-get install Python-bs4`
&nbsp;&nbsp;&nbsp; `sudo apt-get install Python-lxml`
&nbsp;&nbsp;&nbsp; Users work with orther platform should check [bs4 source](https://pypi.python.org/pypi/beautifulsoup4) and [lxml source](https://pypi.python.org/pypi/lxml).

### Usage
- Create a MySQL schema with a specified table first. You could find the SQL script in the package.
- You could run the crawler by executing command `python crawler`.
- You may need to modify some config arguments in \_\_init\_\_.py.
- The parser module may need to be rewrote by yourself.
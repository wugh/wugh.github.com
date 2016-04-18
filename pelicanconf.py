#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Guohua Wu'
SITENAME = u'Life in a Nutshell'
SITEURL = 'https://wugh.github.io'

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh-CN'

# Feed generation is usually not desired when developing
FEED_DOMAIN = 'https://wugh.github.io'
FEED_ATOM = 'feeds/main.atom.xml'
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
# LINKS = (('Pelican', 'http://getpelican.com/'),
#          ('Python.org', 'http://python.org/'),
#          ('Jinja2', 'http://jinja.pocoo.org/'),)

# Social widget
SOCIAL = (('GitHub', 'https://github.com/wugh'),)

DEFAULT_PAGINATION = 10

# 插件
PLUGIN_PATHS = ['../pelican-plugins']
PLUGINS = ['render_math']

# 主题
THEME = '../pelican-themes/pelican-octopress-theme'
MENUITEMS = [('Archives', '/archives.html')]
DISQUS_SITENAME = 'guohuasblog'

# 导航
DISPLAY_CATEGORIES_ON_MENU = False

# HTML优化
TYPOGRIFY = True

# 文章路径优化
ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{slug}/index.html'

DATE_FORMATS = {
    'zh-cn': '%Y-%m-%d(%a)'
}

# Google Analytics
GOOGLE_UNIVERSAL_ANALYTICS = 'UA-52495737-1'

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# add customer filter
import os
import sys
sys.path.append(os.curdir)
from hashing import md5s as md5hash
JINJA_FILTERS = {
    "md5hash": md5hash
}

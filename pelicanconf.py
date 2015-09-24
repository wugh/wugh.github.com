#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Guohua Wu'
SITENAME = u'Life in a Nutshell'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = u'zh-CN'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# 插件
PLUGIN_PATHS = ['pelican-plugins']
PLUGINS = ['render_math']

# 主题
THEME = './Nuja'
MENUITEMS = [('Archives', '/archives.html')]
DUOSHUO = 'wughblog'

# HTML优化
TYPOGRIFY = True

# 文章路径优化
ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{slug}/index.html'

DATE_FORMATS = {
    'zh-cn': '%Y-%m-%d(%a)'
}

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

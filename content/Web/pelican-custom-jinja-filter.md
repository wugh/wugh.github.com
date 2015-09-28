title: Pelican自定义Jinja过滤器
date: 2015-09-28 10:18
category: Web
tags: Pelican, Jinja, Filter
slug: pelican-custom-jinja-filter

使用`Pelican`的时候发现需要在模板中使用`Hash`函数，但是`Jinja`并没有提供`Hash`
过滤器，需要自己实现一个`Hash`过滤器，这里以`Hash`过滤器为例子讲讲如何在
`Pelican`中使用自定义过滤器。

### Hash函数功能实现

通过`Python`的标准库函数实现一个`md5`的哈希函数，函数的功能的是传入一个字符串
返回该字符串的`md5`串，实现如下：

	:::python
	# (c) 2012-2014, Michael DeHaan <michael.dehaan@gmail.com>
	#
	# This file is part of Ansible
	#
	# Ansible is free software: you can redistribute it and/or modify
	# it under the terms of the GNU General Public License as published by
	# the Free Software Foundation, either version 3 of the License, or
	# (at your option) any later version.
	#
	# Ansible is distributed in the hope that it will be useful,
	# but WITHOUT ANY WARRANTY; without even the implied warranty of
	# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	# GNU General Public License for more details.
	#
	# You should have received a copy of the GNU General Public License
	# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

	# Make coding more python3-ish
	from __future__ import (absolute_import, division, print_function)
	__metaclass__ = type


	# Note, sha1 is the only hash algorithm compatible with python2.4 and with
	# FIPS-140 mode (as of 11-2014)
	try:
		from hashlib import sha1 as sha1
	except ImportError:
		from sha import sha as sha1

	# Backwards compat only
	try:
		from hashlib import md5 as _md5
	except ImportError:
		try:
			from md5 import md5 as _md5
		except ImportError:
			# Assume we're running in FIPS mode here
			_md5 = None

	def secure_hash_s(data, hash_func=sha1):
		''' Return a secure hash hex digest of data. '''

		digest = hash_func()
		try:
			if not isinstance(data, basestring):
				data = "%s" % data
			digest.update(data)
		except UnicodeEncodeError:
			digest.update(data.encode('utf-8'))
		return digest.hexdigest()


	# The checksum algorithm must match with the algorithm in ShellModule.checksum() method
	checksum_s = secure_hash_s

	# Backwards compat functions.  Some modules include md5s in their return values
	# Continue to support that for now.  As of ansible-1.8, all of those modules
	# should also return "checksum" (sha1 for now)
	# Do not use md5 unless it is needed for:
	# 1) Optional backwards compatibility
	# 2) Compliance with a third party protocol
	#
	# MD5 will not work on systems which are FIPS-140-2 compliant.


	def md5s(data):
		if not _md5:
			raise ValueError('MD5 not available.  Possibly running in FIPS mode')
		return secure_hash_s(data, _md5)
这里的`md5s`实现了我们需要的功能。

### 向Pelican注册Jinja过滤器

通过配置`Pelican`的配置文件`pelicanconf.py`注册过滤器的名字和对应的函数，如下：

	:::python
	# add customer filter
	import os
	import sys
	sys.path.append(os.curdir)
	from hashing import md5s as md5hash
	JINJA_FILTERS = {
		"md5hash": md5hash
	}
代码中注册了一个名字为`md5hash`的过滤器，并且对应的函数名字也叫`md5hash`。

### 在Jinja模板中使用自定义过滤器
下面的模板中通过文章的`url`产生一个唯一的`key`给多说插件使用
`data-thread-key="{{ article.url|md5hash }}"`

	:::html
	{%if DUOSHUO %}
	<div class="row">
		<div class="alpha span9">
				<!-- 多说评论框 start -->
				<!--data-thread-key="的ID"-->
				<div class="ds-thread" data-thread-key="{{ article.url|md5hash }}" data-title="{{ article.title|striptags }}" data-url="{{article.url}}"></div>
				<!-- 多说评论框 end -->
				<!-- 多说公共JS代码 start (一个网页只需插入一次) -->
				<script type="text/javascript">
				var duoshuoQuery = {short_name:"{{DUOSHUO}}"};
					(function() {
						var ds = document.createElement('script');
						ds.type = 'text/javascript';ds.async = true;
						ds.src = (document.location.protocol == 'https:' ? 'https:' : 'http:') + '//static.duoshuo.com/embed.js';
						ds.charset = 'UTF-8';
						(document.getElementsByTagName('head')[0] 
						 || document.getElementsByTagName('body')[0]).appendChild(ds);
					})();
					</script>
				<!-- 多说公共JS代码 end -->
	</div></div>
	{%endif%}


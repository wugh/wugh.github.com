title: Gentoo Portage使用技巧
date: 2013-11-09 10:06:01
category: Linux
tags: Portage, Gentoo
slug: gentoo-portage-tips
---

本文章记录一些使用Gentoo Portage的技巧。
### 指定Slot安装软件
`Slot`是在`Gentoo`的包管理的一个重要功能，当一个软件有多个分支的时候Portage能够
保证不同的版本并存。例如，Python一般有多个版本

	:::bash
	$ eix dev-lang/python
	[I] dev-lang/python
		 Available versions:  
			(2.5)   2.5.4-r4 ~2.5.4-r5
			(2.6)   2.6.8 ~2.6.8-r1
			(2.7)   2.7.3-r2 ~2.7.3-r3
			(3.1)   3.1.5 ~3.1.5-r1
			(3.2)   3.2.3 ~3.2.3-r1 ~3.2.3-r2
			(3.3)   **3.3.0 **3.3.0-r1

上面的搜索出来的记过中括号中的就是slot号码，那么如何根据slot安装不同的软件呢，
下面将会解释这一点。

	:::bash
	$ emerge -pv dev-lang/python:3.3

通过上面的方式就可以安装Python3.3。

### emerge特定版本的软件
使用`emerge`搜索`gitolite`，出现的结果很多，如果我们不想安装默认的版本那么就得
用特定的命令。

	:::bash
	tom@nextzone ~ $ eix dev-vcs/gitolite
	* dev-vcs/gitolite
		 Available versions:  2.3.1 ~3.1 ~3.2 ~3.3 ~3.4 ~3.5 ~3.5.1 ~3.5.2 {contrib tools vim-syntax}
		 Homepage:            http://github.com/sitaramc/gitolite
		 Description:         Highly flexible server for git directory version tracker
安装`3.5.2`的方法如下：

	:::bash
	emerge --ask =dev-vcs/gitolite-3.5.2

### emerge的正则搜索
`emerge --search "package name"`是一个正常使用方法，如果待搜索的名字是以`%`开头
那么代表这个是一个正则表达式。例如，`emerge --search "%^kde"`会搜索出全部以
`kde`开头的包，但是要注意的是，这样子搜索的时候不匹配软件包所在的类别，如果要匹
配类别，那么就需要加上`@`：就可以搜索`dev-java`这个类别下含有`jdk`关键词的软件
包。

	:::bash
	guohuawu@cist-tux ~ $ emerge --search "%@^dev-java.*jdk"
	Searching...    
	[ Results for search key : ^dev-java.*jdk ]
	[ Applications found : 11 ]

	*  dev-java/apple-jdk-bin [ Masked ]
		  Latest version available: 1.6.0
		  Latest version installed: [ Not Installed ]
		  Size of files: 0 kB
		  Homepage:      http://java.sun.com/j2se/1.6.0/
		  Description:   Links to Apple's version of Sun's J2SE Development Kit
		  License:       public-domain

	*  dev-java/db4o-jdk11
		  Latest version available: 7.4
		  Latest version installed: [ Not Installed ]
		  Size of files: 312 kB
		  Homepage:      http://www.db4o.com
		  Description:   Core files for the object database for java
		  License:       GPL-2

### eix
上面提到用`emerge`来搜索软件包，但是这个方法遇到的一个最大问题就是搜索非常慢，
用`eix`可以解决这个问题。

	:::bash
	root # emerge --ask eix
这样以来同步Portage就变得非常简单：

	:::bash
	root # eix-sync
通用`eix`也支持正则搜索，而且搜索速度非常快

	:::bash
	guohuawu@cist-dell ~ $ eix ^ack$
	[I] sys-apps/ack
		 Available versions:  1.96 2.12 {test}
		 Installed versions:  2.12(06:48:04 PM 05/24/2014)(-test)
		 Homepage:            http://betterthangrep.com/ http://search.cpan.org/dist/ack/
		 Description:         ack is a tool like grep, aimed at programmers with large trees of heterogeneous source code
下面举出一些常用的例子

* `eix kernel`：搜索含有kernel关键词的包
* `eix -I kernel`：从已经安装的包里面搜索
* `eix -S -c corba`：搜索包的描述，并且用紧凑模式输出
* `eix -C -c app-officeext`：搜索一个类别的包，，并且用紧凑模式输出

更多的请参考[Gentoo Wiki](http://wiki.gentoo.org/wiki/Eix)。

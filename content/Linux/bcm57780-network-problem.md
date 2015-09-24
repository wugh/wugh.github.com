title: BCM57780没有网络连接
date: 2013-11-10 00:16:36
category: Linux
tags: 内核编译, Gentoo
slug: bcm57780-network-problem
---

### 问题描述
安装完Gentoo之后发现系统一直没有办法上网，通过`lspci`找到自己的网卡之后，搜索问
题，发现通过下面几条命令之后才能够激活网卡：

	:::bash
	# rmmod broadcom 
	# rmmod tg3 
	# modprobe broadcom 
	# modprobe tg3 
	# dhcpcd eth0 

### 问题解决
但是并不能永久解决问题，由上面看来问题应该出在内核那边，需要安装下面的方法重新
编译一下模块：

	:::bash
	Device Drivers ---> 
		 Network Device Support ---> 
			  Ethernet driver support ---> 
				   Broadcom devices 
					 <M> Broadcom Tigon3 support 
			  PHY Device support and infrastrcutre ---> 
				 <M> Drivers for Broadcom PHYs

### 参考文章
* [No Connection with BCM57780 After Installing]

[No Connection with BCM57780 After Installing]:http://forums.gentoo.org/viewtopic-t-925416-start-0.html

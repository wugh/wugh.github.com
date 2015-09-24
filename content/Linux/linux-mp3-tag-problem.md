title: 解决Linux下mp3标签乱码
date: 2013-11-09 09:29:46
category: Linux
tags: mp3,乱码
slug: linux-mp3-tag-problem
---

在Linux下mp3标签出现乱码的原因主要是下载到的mp3都使用[GB2312](http://zh.wikipedia.org/wiki/GB_2312)编码，然而Linux下使用的编码是[UTF-8](http://zh.wikipedia.org/wiki/UTF-8)编码，所以只要对标签编码做一个转换就可以解决问题。

### 安装软件
下面以Gentoo为例子安装[Mutagen](https://code.google.com/p/mutagen/)，其他的发行
版自行Google。
```bash
emerge --ask media-libs/mutagen
```

### 转换当前目录下的所有mp3文件标签
```bash
find . -iname "*.mp3" -exec mid3iconv -e gbk {} \;
```

### 转换当前目录下的所有ape文件标签
```bash
find . -iname "*.ape" -exec mid3iconv -e gbk {} \;
```

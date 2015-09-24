title: Linux字体配置
date: 2013-11-09 09:54:23
category: Linux
tags: fontconfig
slug: linux-fontconfig
---

### fontconfig简介
Linux字体配置采用
[fontconfig](http://www.freedesktop.org/wiki/Software/fontconfig/)来做字体渲染
，中文的[fontconfig手册
](http://codex.wordpress.org.cn/Fontconfig%E7%94%A8%E6%88%B7%E6%89%8B%E5%86%8C)
参考这里，根据这个手册对Linux的字体进行简单的配置。

### 配置文件
根据自己的日常使用习惯，下面对我的fontconfig配置文件做一个描述。

#### dpi设定

dpi的详细设定参考这两篇文章，[dpi设置及sub-pixel次像素微调
](http://xxb.is-programmer.com/posts/4260.html)和[Linux 字体微调 - windows 效果
版](http://www.linuxsir.org/bbs/thread266659.html)两篇文章，Windows 7的默认dpi
是96，我的字体设定的dpi也采用96。参考前面两篇文章可以知道dpi的计算公式如下：
```text
屏幕 width = 287 mm = 28.7 cm，height = 215 mm = 21.5 cm
水平 dpi = 水平 resolution * 2.54 / width = 1024 * 2.54 / 28.7 = 90.6 
垂直 dpi = 垂直 resolution * 2.54 / height = 768 * 2.54 / 21.5 = 90.7
```
计算得到dpi就可以在fontconfig里面设定：
```xml
<match target="pattern">
	<edit name="dpi" mode="assign" >
		<double>96</double>
	</edit>
</match>
```

#### 抗锯齿
抗锯齿设定可以增加字体边缘的分辨率，配置如下
```xml
<match target="font">
	<edit mode="assign" name="antialias">
		<bool>true</bool>
	</edit>
</match>
```

#### 字体微调
使用普通微调，TrueType微调指令会被freetype的字节码解释器所解释，对于那些有好的
微调指令的字体是一个好选择，然后选择的微调效果是`hintslight`。
```xml
<match target="font">
	<edit mode="assign" name="hinting">
		<bool>true</bool>
	</edit>
</match>
<match target="font">
	<edit mode="assign" name="hintstyle">
		<const>hintslight</const>
	</edit>
</match>
```

#### 次像素渲染
次像素渲染能通过使用次像素有效地提高字体的水平（垂直）分辨率。注意在没有使用
[Infinality](http://www.infinality.net/blog/)补丁的情况下autohint和subpixel
rendering不能一起使用。通常情况下现在的显示器使用宏红、绿、蓝（RGB）标准生产，
所以大多数情况下把次像素渲染类型设定为`RGB`。
```xml
<match target="font">
<edit mode="assign" name="rgba">
		<const>rgb</const>
	</edit>
</match>
```

当使用次像素渲染的时候需要开启[LCD
filter](http://www.freetype.org/freetype2/docs/reference/ft2-lcd_filtering.html)
（液晶过滤），这个选项的取值一般来说选`lcddefault`就可以，完整取值请参考
fontconfig手册。
```xml
<match target="font">
<edit mode="assign" name="lcdfilter">
		<const>lcddefault</const>
	</edit>
</match>
```

### 字体替换
这里简要说明以下字体替换，替换的简洁写法是采用`alias`标签。在`family`标签里面写
好要替换的字体族名字，然后最后那个`prefer`标签的意思是，在匹配的字体列表前面插
入一些列的字体名字。需要注意的是这个列表里面的字体应该有一些是你的系统里面有的
。

Gentoo安装一些要用到的字体：
```bash
emerge media-fonts/corefonts #ms core font
emerge media-fonts/dejavu #DejaVu fonts
emerge media-fonts/ttf-bitstream-vera #Bitstream Vera font family
emerge media-fonts/arphicfonts #ukai uming等字体
emerge wqy-bitmapfont wqy-microhei wqy-zenhei #文泉驿字体
```
还需要一些雅黑、宋体一类的字体，就可以自己从windows下复制，最后字体替换顺序如下：
```xml
<alias>
	<family>serif</family>
	<prefer>
		<family>DejaVu Serif</family>
		<family>Bitstream Vera Serif</family>
		<family>Times New Roman</family>
		<family>SimSun</family>
		<family>AR PL New Sung</family>
		<family>AR PL ShanHeiSun Uni</family>
	</prefer>
</alias>

<alias>
	<family>sans-serif</family>
	<prefer>
		<family>Arial</family>
		<family>Open Sans</family>
		<family>Microsoft YaHei</family>
		<family>WenQuanYi Micro Hei</family>
	</prefer>
</alias>

<alias>
	<family>monospace</family>
	<prefer>
		<family>PowerlineSymbols</family>
		<family>Inconsolata</family>
		<family>WenQuanYi Zen Hei Mono</family>
		<family>WenQuanYi Micro Hei Mono</family>
		<family>Arial Unicode MS</family>
	</prefer>
</alias>
```

### 部署配置文件
通过以上步骤就能获得一个fontconfig配置文件，文件比较长，就不再复制过来，可以从
我的[gist](https://gist.github.com/wugh/7386376)下载，下载完之后把文件放到HOME
目录下，重新命名为`.fonts.conf`，不过这种方法快要被fontconfig抛弃了，现在建议的
做法是把文件放到`~/.config/fontconfig/conf.d/`下命名的时候在前面加个数字，表示
一个优先级，操作如下：
```bash
mkdir -p ~/.config/fontconfig/conf.d/
mv fonts.conf ~/.config/fontconfig/conf.d/40-myfonts.conf
```
重启X Server之后就能看到生效的字体效果。

### 参考文章
* [Archlinux Font Configuration](https://wiki.archlinux.org/index.php/Font_Configuration)
* [fonts-conf document](http://www.freedesktop.org/software/fontconfig/fontconfig-user.html)
* [fontconfig中文文档](http://codex.wordpress.org.cn/Fontconfig用户手册)

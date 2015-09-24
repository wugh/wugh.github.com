title: Linux 音频格式转换
date: 2013-11-09 09:15:30
category: Linux
tags: 格式转换
slug: linux-audio-format-convert
---
### 需要的软件

在开始转换之前我们需要两个程序[LAME](http://lame.sourceforge.net/download.php)
和[FAAD2](http://www.audiocoding.com/downloads.html)，这两个包应该通过linux自带
的软件包管理器就可以安装。Gentoo下面安装方法如下：
``` bash
emerge --ask media-sound/lame
emerge --ask media-libs/faad2
```

### 批量转换

#### m4a转换成mp3

```bash
#!/bin/bash

for i in *.m4a; do
    echo "Converting: ${i%.m4a}.mp3"
    faad -o - "$i" | lame - "${i%.m4a}.mp3"
done
```

#### flac转mp3
另外可以使用flac转mp3，需要以下三个命令flac lame id3，然后使用以下脚本
```bash
#! /bin/sh

for a in *.flac; do
    OUTF=${a%.flac}.mp3

    ARTIST=$(metaflac "$a" --show-tag=ARTIST | sed s/.*=//g)
    TITLE=$(metaflac "$a" --show-tag=TITLE | sed s/.*=//g)
    ALBUM=$(metaflac "$a" --show-tag=ALBUM | sed s/.*=//g)
    GENRE=$(metaflac "$a" --show-tag=GENRE | sed s/.*=//g)
    TRACKNUMBER=$(metaflac "$a" --show-tag=TRACKNUMBER | sed s/.*=//g)
    DATE=$(metaflac "$a" --show-tag=DATE | sed s/.*=//g)

    flac -c -d "$a" | lame -m j -q 0 --vbr-new -V 0 -s 44.1 - "$OUTF"
    id3 -t "$TITLE" -T "${TRACKNUMBER:-0}" -a "$ARTIST" -A "$ALBUM" -y "$DATE" -g "${GENRE:-12}" "$OUTF"
done
```

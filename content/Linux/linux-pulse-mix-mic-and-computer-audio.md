title: Linux通过Pulse混合麦克风和音频输出
date: 2015-01-08 21:08
category: Linux
tags: pulse,录音
slug: linux-pulse-mix-mic-and-computer-audio
---

由于想在语音识别时候给麦克风加噪声，所以就在思考有没有办法通过混合麦克风输入和
电脑的音频输出混合起来实现加噪声的效果呢？经过Google找到以下的[解决办法
](https://www.youtube.com/watch?v=8hkCE7ETJRM)，这种方法依赖
[PulseAudio](http://zh.wikipedia.org/wiki/PulseAudio "PulseAudio")。

### 安装工具
首先需要安装
[pavucontrol](http://freedesktop.org/software/pulseaudio/pavucontrol/)用来管理
Pulse。

	:::bash
	emerge -a media-sound/pavucontrol

### 修改配置文件
修改配置文件`/etc/pulse/default.pa`，添加以下模块

	:::bash
	load-module module-null-sink 
	load-module module-loopback
	load-module module-loopback
然后重启电脑或者重启Pulse服务器。

上面的步骤也可以不重启Pulse服务器，直接通过`pacmd`这个命令行工具配置Pulse服务
器，可以在这个命令行的交互工具中，执行以上三个命令。

### 通过pavucontrol配置音频混合

我们添加了两个loopback，这时候就可以在pavucontrol的Playback标签页下面看到
两个新的Loopback，需要把`Show`这个过滤器选择为`All Streams`，结果如下图所示：
![Playback]({filename}/images/Linux/playback.png "Playback")
这两个Loopback一个是麦克风（Loopback from Bulit-in Audio Analog Stero）另一个
是电脑的音频输出（Loopback of Monitor of Bult-in Audio Analog Stero），需要把
这两个的输出设定成`Null Output`。

接着需要设定一下我们录音的时候使用哪个声音源，设置如下图
![Record]({filename}/images/Linux/record.png "Record")
可以看到`ALSA Capture from`被我们设置成`Monitor of Null Output`，相当于把Null
这个设备的输出当作声音源进行捕获，而Null这个设备输出是麦克风和电脑声音的混合，
所以可以正常工作。


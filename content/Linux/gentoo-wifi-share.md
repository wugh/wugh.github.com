title: gentoo wifi 共享
date: 2013-11-09 00:57:27
category: Linux
tags: hostapd,ap,Gentoo
slug: gentoo-wifi-share
---
### 简介
本文主要描述如何在`Gentoo`下利用无线网卡做一个`wifi`热点来给手机提供无线网络访
问。目前在`Windows`下有[connectify]来共享网络，同样的在`Linux`下也有[hostapd]。
由于在Windows下基本就是一键配置热点，但是Linux配置起来比较麻烦，所以本文在这里
记录一下配置过程。

### 软件安装
需要安装一些软件
```bash
emerge -a hostapd
emerge -a dnsmasq
emerge -a iptables
```

### 配置
以下描述各个软件的配置说明。

#### 网卡参数
修改文件`/etc/conf.d/net`：
```bash
modules_wlan0="!iwconfig !wpa_supplicant"
config_wlan0="192.168.0.1/24"
```

网卡配置好之后，要加入默认启动。
```bash
cd /etc/init.d
ln -s net.lo net.wlan0
/etc/init.d/net.wlan0 start
rc-update add net.wlan0 default
```

#### hostapd配置
修改`hostapd`配置文件`/etc/hostapd/hostapd.conf`：
```bash
interface=wlan0
#bridge=br0                         (optional, if you want bridging remove the #)
driver=nl80211
ssid=MyNetwork     #热点名称
channel=1
hw_mode=g
wpa=3
wpa_passphrase=Your passphrase  #热点密码
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
logger_syslog=-1
logger_syslog_level=2
logger_stdout=-1
logger_stdout_level=1
debug=0
dump_file=/tmp/hostapd.dump
ctrl_interface=/var/run/hostapd
ctrl_interface_group=0
accept_mac_file=/etc/hostapd/hostapd.accept
deny_mac_file=/etc/hostapd/hostapd.deny
auth_algs=1
```
把hostapd加入默认启动。
```bash
/etc/init.d/hostapd start
rc-update add hostapd default
```
#### dnsmasq配置
修改`dnsmasq`配置文件`/etc/dnsmasq.conf`：
```bash
interface=wlan0
bind-interfaces
dhcp-range=192.168.0.50,192.168.0.150,12h
```
dnsmasq用来分配IP，所以要启动这个服务。
```bash
/etc/init.d/dnsmasq start
rc-update add dnsmasq default
```
#### iptables配置
iptables用来设置包的转发规则，以NAT方式配置AP。
```bash
iptables -F
iptables -t nat -F
iptables -A FORWARD -i wlan0 -s 192.168.0.0/255.255.0.0 -j ACCEPT
iptables -A FORWARD -i eth0 -d 192.168.0.0/255.255.0.0 -j ACCEPT
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
echo 1 > /proc/sys/net/ipv4/ip_forward
```
保存规则，并把iptable默认启动
```
/etc/init.d/iptables save
rc-update add iptables default
```

### 总结
以上这些东西配置后之后，我们的手机应该就可以连上的点的wifi热点。

### 参考
* [Atheros Ath5k/Ath9k Wireless Access Point](http://en.gentoo-wiki.com/wiki/Atheros_Ath5k/Ath9k_Wireless_Access_Point#Without_Ethernet_Bridging)
* [Wireless/Access point](http://en.gentoo-wiki.com/wiki/Wireless/Access_point)


[connectify]:http://www.connectify.me/
[hostapd]:http://linuxwireless.org/en/users/Documentation/hostapd

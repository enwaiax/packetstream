# packetstream
<!-- PROJECT SHIELDS -->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]

<!-- PROJECT LOGO -->
<br />
<p align="center">
  <br>
    <img src="https://packetstream.io/assets/images/logo.png?cb=1614583587" alt="PacketStream Logo" width="33" height="38">
    <h3 align="center">PacketStream</br>
  </br>
  <h3 align="center">Docker image for PacketStream</h3>
  <p align="center">分享闲置家用带宽获得利润: $0.10/GB</p>
  <p align="center">
    <a href="https://github.com/Chasing66/PacketStream" target="_blank">Github</a>
    |
    <a href="https://hub.docker.com/r/enwaiax/PacketStream" target="_blank">Docker Hub</a>
  </p>
</p>

## MJJ
- 请低调使用，张弛有度

## 充电支持

<a href="https://afdian.net/@LuckyHunter"><img src="https://img.shields.io/badge/%E7%88%B1%E5%8F%91%E7%94%B5-LuckyHunter-%238e8cd8?style=for-the-badge" alt="前往爱发电赞助" width=auto height=auto border="0" /></a>

## 介绍
- 本项目基于Alpine docker 镜像搭建PacketStream容器，实现在单个VPS上同时并发运行多个进程，可以获得多倍的流量。脚本包括自动增加虚拟内存（物理内存的两倍）、安装docker、安装docke-compose、设置CID、设置运行容器数量等。
- 脚本会自动检测是否满足Residential IP条件，若不满足会自动删除所有容器，并退出进程
- 若本地无实际Residential IP带宽, 支持设置Residential代理来运行
- 可以和[peer2profit](https://github.com/Chasing66/peer2profit)同时运行

## 信息
- 本项目已经在 Ubuntu16+ 和 Debian10+上验证
- 必须住宅IP，可使用住宅代理。如需快捷开启http代理，推荐使用[x-ui](https://github.com/Chasing66/beautiful_docker/tree/main/x-ui)docker 版本
- 开发不易，如果你想尝试，请通过我的推荐链接注册。 [推荐链接](https://packetstream.io/?psr=2HVV)


### 使用方法
```shell
mkdir PacketStream && cd PacketStream
wget -Nnv https://raw.githubusercontent.com/Chasing66/PacketStream/main/packetstream.py &>/dev/null
chmod +x packetstream.py
python3 packetstream.py -c "你的CID" -n "容器数量" -p "http代理"
```
#### 例如
```shell
mkdir PacketStream && cd PacketStream
wget -Nnv https://raw.githubusercontent.com/Chasing66/PacketStream/main/packetstream.py &>/dev/null
chmod +x packetstream.py
python3 packetstream.py -c 2HVV -n 5
```
#### 使用代理
```shell
python3 packetstream.py -c 2HVV -n 5 -p "http://exampele.com:27015"
```

### 免责声明

本程序仅供学习了解, 非盈利目的，请于下载后 24 小时内删除, 不得用作任何商业用途, 文字、数据及图片均有所属版权, 如转载须注明来源。

使用本程序必循遵守部署免责声明。使用本程序必循遵守部署服务器所在地、所在国家和用户所在国家的法律法规, 程序作者不对使用者任何不当行为负责.

### 鸣谢
- [Pony](https://peer2profit.net/)
- a^小怪

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/Chasing66/PacketStream.svg?style=for-the-badge
[contributors-url]: https://github.com/Chasing66/PacketStream/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Chasing66/PacketStream.svg?style=for-the-badge
[forks-url]: https://github.com/Chasing66/PacketStream/network/members
[stars-shield]: https://img.shields.io/github/stars/Chasing66/PacketStream.svg?style=for-the-badge
[stars-url]: https://github.com/Chasing66/PacketStream/stargazers
[issues-shield]: https://img.shields.io/github/issues/Chasing66/PacketStream.svg?style=for-the-badge
[issues-url]: https://github.com/Chasing66/PacketStream/issues
[license-shield]: https://img.shields.io/github/license/Chasing66/PacketStream.svg?style=for-the-badge
[license-url]: https://github.com/Chasing66/PacketStream/blob/main/LICENSE

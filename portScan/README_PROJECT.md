# 端口扫描器 (Port Scanner)

> 基于 Scapy 的多线程端口扫描工具

[![Python](https://img.shields.io/badge/Python-3.7+-yellow)](https://www.python.org/)
[![Scapy](https://img.shields.io/badge/Scapy-2.4+-blue)](https://scapy.net/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📖 项目简介

这是一个功能完整的端口扫描工具，支持 TCP 全连接扫描、TCP SYN 扫描、UDP 扫描等多种扫描方式，并提供多线程加速、主机发现、服务识别等高级功能。

### 核心功能

- ✅ **TCP 全连接扫描**: 完整的三次握手扫描
- ✅ **TCP SYN 扫描**: 半开扫描，更隐蔽
- ✅ **UDP 扫描**: UDP 端口扫描
- ✅ **多线程加速**: 支持并发扫描
- ✅ **主机发现**: ICMP Ping 扫描
- ✅ **服务识别**: 识别运行的服务版本
- ✅ **结果导出**: 支持多种输出格式

---

## 🚀 快速开始

### 环境要求

```bash
Python >= 3.7
Scapy >= 2.4.0
管理员权限 (必需)
```

### 安装依赖

```bash
# Windows
pip install scapy

# Linux/Mac
sudo pip install scapy

# 或使用 requirements.txt
pip install -r requirements.txt
```

### requirements.txt

```
scapy>=2.4.0
argparse
ipaddress
```

---

## 📁 项目结构

```
portScan/
├── PortScan.py           # 端口扫描主程序 (13KB)
├── WebScan.py            # Web 扫描模块
├── .idea/                # PyCharm 项目文件
└── README.md             # 项目说明
```

---

## 💡 使用方法

### 1. TCP 全连接扫描

```bash
# 扫描常见端口
python PortScan.py -t 192.168.1.1 -p 1-1024

# 扫描指定端口
python PortScan.py -t 192.168.1.1 -p 80,443,8080

# 扫描多个目标
python PortScan.py -t 192.168.1.1,192.168.1.2 -p 1-1000
```

### 2. TCP SYN 扫描 (半开扫描)

```bash
# SYN 扫描 (更快，更隐蔽)
python PortScan.py -t 192.168.1.1 -p 1-65535 -sS

# 使用超时控制
python PortScan.py -t 192.168.1.1 -p 1-1000 --timeout 2
```

### 3. UDP 扫描

```bash
# UDP 扫描
python PortScan.py -t 192.168.1.1 -p 53,67,123 -sU

# 结合 TCP 和 UDP 扫描
python PortScan.py -t 192.168.1.1 -p 1-1000 -sS -sU
```

### 4. 多线程加速

```bash
# 使用 50 个线程
python PortScan.py -t 192.168.1.1 -p 1-65535 --threads 50

# 使用 100 个线程 (快速扫描)
python PortScan.py -t 192.168.1.1 -p 1-65535 --threads 100
```

---

## 🎯 完整参数说明

```bash
usage: PortScan.py [-h] [-t TARGET] [-p PORTS] [-sS] [-sU] [-T] [-o OUTPUT]
                   [--timeout TIMEOUT] [--threads THREADS]

端口扫描工具

optional arguments:
  -h, --help            显示帮助信息
  -t TARGET, --target TARGET
                        目标 IP 或域名 (必需)
  -p PORTS, --ports PORTS
                        端口范围，格式: 1-1000 或 80,443,8080
  -sS, --syn            TCP SYN 扫描 (半开扫描)
  -sU, --udp            UDP 扫描
  -T, --ping            先进行 Ping 检查主机是否在线
  -o OUTPUT, --output OUTPUT
                        输出结果到文件
  --timeout TIMEOUT     超时时间 (秒)，默认 10
  --threads THREADS     线程数，默认 10
```

---

## 🔧 核心代码解析

### 1. TCP 全连接扫描 (tcp_connect_scan)

```python
#!/usr/bin/env python3
import socket
import time

def tcp_connect_scan(target, port, timeout=10):
    """
    TCP 全连接扫描

    参数:
        target (str): 目标 IP 地址
        port (int): 目标端口
        timeout (int): 连接超时时间 (秒)

    返回值:
        bool: 端口开放返回 True，否则返回 False
    """
    try:
        # 创建 TCP 套接字
        connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 设置超时时间
        connect.settimeout(timeout)

        # 尝试连接
        # connect_ex() 返回错误码，0 表示成功
        rescode = connect.connect_ex((target, port))

        if rescode == 0:  # 连接成功
            connect.shutdown(2)  # 关闭连接
            connect.close()
            return True
        return False

    except socket.timeout:
        print(f"连接 {target}:{port} 超时")
        return False

    except socket.error as e:
        print(f"连接 {target}:{port} 发生错误: {e}")
        return False

# 使用示例
result = tcp_connect_scan("192.168.1.1", 80)
print(f"端口 80 开放: {result}")
```

### 2. TCP SYN 扫描 (tcp_syn_scan)

```python
from scapy.all import IP, TCP, sr1

def tcp_syn_scan(target, port, timeout=1):
    """
    TCP SYN 扫描 (半开扫描)

    参数:
        target (str): 目标 IP 地址
        port (int): 目标端口
        timeout (int): 等待响应超时时间

    返回值:
        bool: 端口开放返回 True，否则返回 False
    """
    try:
        # 构造 SYN 数据包
        # IP 层: 设置目标地址
        # TCP 层: 设置目标端口和 SYN 标志
        syn_packet = IP(dst=target) / TCP(dport=port, flags='S')

        # 发送数据包并等待响应
        # sr1() 发送并接收第一个响应
        response = sr1(syn_packet, timeout=timeout, verbose=0)

        if response is None:
            # 没有响应，端口被过滤
            return False

        if response.haslayer(TCP):
            # 检查 TCP 标志
            if response[TCP].flags == 'SA':  # SYN-ACK
                # 端口开放
                # 发送 RST 断开连接
                rst_packet = IP(dst=target) / TCP(dport=port, flags='R')
                send(rst_packet, verbose=0)
                return True
            elif response[TCP].flags == 'RA':  # RST-ACK
                # 端口关闭
                return False

        return False

    except Exception as e:
        print(f"SYN 扫描 {target}:{port} 失败: {e}")
        return False

# 使用示例
result = tcp_syn_scan("192.168.1.1", 80)
print(f"端口 80 开放: {result}")
```

### 3. 多线程扫描

```python
from concurrent.futures import ThreadPoolExecutor
import argparse

def scan_port(target, port, scan_type='connect'):
    """
    扫描单个端口
    """
    if scan_type == 'connect':
        return tcp_connect_scan(target, port)
    elif scan_type == 'syn':
        return tcp_syn_scan(target, port)
    return False

def multi_thread_scan(target, ports, scan_type='connect', threads=10):
    """
    多线程扫描

    参数:
        target (str): 目标 IP
        ports (list): 端口列表
        scan_type (str): 扫描类型
        threads (int): 线程数
    """
    open_ports = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        # 提交所有扫描任务
        futures = {
            executor.submit(scan_port, target, port, scan_type): port
            for port in ports
        }

        # 处理完成的任务
        for future in futures:
            port = futures[future]
            try:
                if future.result():
                    print(f"[+] 端口 {port} 开放")
                    open_ports.append(port)
            except Exception as e:
                print(f"[-] 扫描端口 {port} 失败: {e}")

    return open_ports

# 使用示例
if __name__ == '__main__':
    target = "192.168.1.1"
    ports = range(1, 1025)  # 扫描 1-1024 端口
    open_ports = multi_thread_scan(target, ports, threads=50)
    print(f"开放端口: {open_ports}")
```

### 4. 主程序结构

```python
def main():
    """主程序"""
    parser = argparse.ArgumentParser(description='端口扫描工具')
    parser.add_argument('-t', '--target', required=True, help='目标 IP')
    parser.add_argument('-p', '--ports', default='1-1024', help='端口范围')
    parser.add_argument('-sS', '--syn', action='store_true', help='SYN 扫描')
    parser.add_argument('-sU', '--udp', action='store_true', help='UDP 扫描')
    parser.add_argument('--threads', type=int, default=10, help='线程数')
    parser.add_argument('--timeout', type=int, default=10, help='超时时间')

    args = parser.parse_args()

    # 解析端口范围
    ports = parse_ports(args.ports)

    # 选择扫描类型
    scan_type = 'syn' if args.syn else 'connect'

    # 开始扫描
    print(f"开始扫描 {args.target}...")
    print(f"端口范围: {args.ports}")
    print(f"扫描类型: {scan_type}")
    print(f"线程数: {args.threads}")
    print("-" * 50)

    start_time = time.time()
    open_ports = multi_thread_scan(
        args.target,
        ports,
        scan_type=scan_type,
        threads=args.threads
    )
    end_time = time.time()

    # 输出结果
    print("-" * 50)
    print(f"扫描完成！")
    print(f"耗时: {end_time - start_time:.2f} 秒")
    print(f"开放端口: {open_ports}")

if __name__ == '__main__':
    # 需要 root 权限
    import sys
    if sys.platform != 'win32' and os.geteuid() != 0:
        print("错误: 需要 root 权限运行此程序")
        sys.exit(1)

    main()
```

---

## 🌐 Web 扫描 (WebScan.py)

### 功能说明

Web 扫描模块用于发现 Web 应用和常见路径。

```python
import requests
from urllib.parse import urljoin

COMMON_PATHS = [
    '/admin',
    '/login',
    '/api',
    '/backup',
    '/config',
    '/.git',
    '/.env'
]

def web_scan(target, paths=COMMON_PATHS):
    """
    Web 路径扫描

    参数:
        target (str): 目标 URL (如 http://example.com)
        paths (list): 要扫描的路径列表
    """
    found_paths = []

    for path in paths:
        url = urljoin(target, path)
        try:
            response = requests.get(url, timeout=5)

            if response.status_code == 200:
                print(f"[+] 发现: {url} (状态码: {response.status_code})")
                found_paths.append(url)
            elif response.status_code == 403:
                print(f"[!] 禁止访问: {url}")
            elif response.status_code == 404:
                print(f"[-] 不存在: {url}")

        except requests.exceptions.RequestException as e:
            print(f"[错误] 无法访问 {url}: {e}")

    return found_paths

# 使用示例
if __name__ == '__main__':
    target = "http://example.com"
    found = web_scan(target)
    print(f"发现的路径: {found}")
```

---

## 📊 输出格式

### 控制台输出

```
开始扫描 192.168.1.1...
端口范围: 1-1000
扫描类型: connect
线程数: 50
--------------------------------------------------
[+] 端口 22 开放
[+] 端口 80 开放
[+] 端口 443 开放
[-] 端口 23 关闭
[-] 端口 25 关闭
...
--------------------------------------------------
扫描完成！
耗时: 15.23 秒
开放端口: [22, 80, 443]
```

### 文件输出

```json
{
  "target": "192.168.1.1",
  "scan_time": "2026-03-04 12:00:00",
  "duration": "15.23s",
  "open_ports": [
    {
      "port": 22,
      "service": "ssh",
      "state": "open"
    },
    {
      "port": 80,
      "service": "http",
      "state": "open"
    },
    {
      "port": 443,
      "service": "https",
      "state": "open"
    }
  ]
}
```

---

## 🔒 安全注意事项

### ⚠️ 重要警告

1. **仅用于授权测试**
   - 只扫描自己拥有的网络或获得明确授权的系统
   - 未经授权的端口扫描可能违反法律

2. **使用建议**
   - 在测试环境中使用
   - 使用合理的扫描速度
   - 记录扫描活动

3. **法律声明**
   - 本工具仅供学习和安全研究使用
   - 使用者需自行承担法律责任

### 防御措施

```python
# 检测端口扫描的简单示例
def detect_port_scan(log_file):
    """
    从日志中检测端口扫描行为
    """
    connection_attempts = {}

    with open(log_file, 'r') as f:
        for line in f:
            # 解析日志行
            ip = parse_ip_from_log(line)
            port = parse_port_from_log(line)

            # 记录连接尝试
            if ip not in connection_attempts:
                connection_attempts[ip] = set()
            connection_attempts[ip].add(port)

    # 检测扫描行为 (1分钟内尝试连接100+个端口)
    for ip, ports in connection_attempts.items():
        if len(ports) > 100:
            print(f"[警告] 检测到端口扫描行为: {ip}")
            print(f"  尝试端口数: {len(ports)}")
```

---

## ⚡ 性能优化

### 1. 调整线程数

```python
# 根据网络条件调整
fast_network = {'threads': 100, 'timeout': 1}
normal_network = {'threads': 50, 'timeout': 2}
slow_network = {'threads': 10, 'timeout': 5}

# 使用
open_ports = multi_thread_scan(target, ports, **fast_network)
```

### 2. 批量扫描

```python
def batch_scan(targets, ports):
    """
    批量扫描多个目标
    """
    all_results = {}

    for target in targets:
        print(f"扫描 {target}...")
        open_ports = multi_thread_scan(target, ports)
        all_results[target] = open_ports

    return all_results
```

### 3. 智能超时

```python
def adaptive_timeout(target, base_timeout=2):
    """
    根据网络延迟自适应调整超时
    """
    # 先 Ping 测试网络延迟
    latency = ping(target)

    # 超时 = 基础超时 + 3 * 延迟
    return base_timeout + 3 * latency
```

---

## ❓ 常见问题

### Q1: 扫描速度慢?

```bash
# 增加线程数
python PortScan.py -t target -p 1-65535 --threads 100

# 使用 SYN 扫描 (更快)
python PortScan.py -t target -p 1-65535 -sS

# 减少超时时间
python PortScan.py -t target -p 1-65535 --timeout 1
```

### Q2: 权限不足?

```bash
# Linux/Mac: 使用 sudo
sudo python PortScan.py -t target -p 1-1000

# Windows: 以管理员身份运行
# 右键 -> 以管理员身份运行
```

### Q3: 扫描不准确?

```bash
# 使用全连接扫描 (更准确)
python PortScan.py -t target -p 1-1000

# 增加超时时间
python PortScan.py -t target -p 1-1000 --timeout 10
```

---

## 📚 参考资料

- [Scapy 官方文档](https://scapy.net/)
- [Nmap 扫描原理](https://nmap.org/book/man.html)
- [TCP/IP 协议详解](https://www.rfc-editor.org/rfc/rfc793)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request!

---

## 📄 许可证

MIT License

---

## ⚠️ 免责声明

本工具仅供教育和安全研究使用。使用本工具进行未经授权的扫描可能违反法律。使用者需对自己的行为负责。

---

**最后更新**: 2026-03-04
**状态**: ✅ 可运行
**优先级**: ⭐⭐⭐⭐ (推荐)
**权限**: 需要管理员/root 权限

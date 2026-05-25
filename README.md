<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/C-Makefile-A8B9CC?logo=c&logoColor=white" alt="C">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
</p>

<h1 align="center">🛡️ Network & Security</h1>

<p align="center">
  网络安全与密码学工具集 — 涵盖加密算法、位置隐私保护、网络扫描与编码工具
</p>

---

## 📑 目录

- [项目概览](#项目概览)
- [项目结构](#项目结构)
- [模块详情](#模块详情)
  - [AES 密钥生成器](#1-aes-密钥生成器-aes_key_generate1)
  - [密码学工具集](#2-密码学工具集-crypto1)
  - [k-匿名位置隐私保护](#3-k-匿名位置隐私保护k匿名位置隐私保护算法)
  - [Netcat 网络工具](#4-netcat-网络工具-netcat)
  - [端口扫描器](#5-端口扫描器-portscan)
  - [URL 编码工具](#6-url-编码工具-urlencode)
- [技术栈](#技术栈)
- [快速开始](#快速开始)
- [许可证](#许可证)

---

## 项目概览

本仓库整合了多个网络安全与密码学方向的实践项目，涵盖以下领域：

| 领域 | 模块 | 语言 |
|:----:|------|:----:|
| 对称加密 | AES 密钥生成器 | Python |
| 非对称加密 & 攻击 | 密码学工具集（RSA/ECC/共模攻击） | Python |
| 位置隐私保护 | k-匿名位置隐私保护算法 | Python |
| 网络调试 | Netcat 网络工具 | C |
| 网络侦察 | 端口扫描器（TCP/UDP/SYN/Web指纹） | Python |
| 编码转换 | URL 编码/解码工具 | Python |

---

## 项目结构

```
NetworkAndSecurity/
├── AES_key_generate1/          # AES 密钥生成工具
│   └── main.py
├── Crypto1/                    # 密码学算法与攻击实现
│   ├── main.py
│   ├── egcd.py
│   └── README_PROJECT.md
├── k匿名位置隐私保护算法/        # k-匿名位置隐私保护算法
│   ├── main.py
│   ├── dataPro.py
│   ├── Figure_*.png
│   ├── anonymized_results_*.csv
│   ├── cluster_info_*.csv
│   ├── random_res_*.csv
│   └── README.md
├── netcat/                     # Netcat 网络调试工具
│   ├── netcat.c
│   ├── doexec.c
│   ├── getopt.c
│   ├── Makefile
│   ├── hobbit.txt
│   └── readme.txt
├── portScan/                   # 端口扫描器
│   ├── PortScan.py
│   ├── WebScan.py
│   └── README_PROJECT.md
├── URLencode/                  # URL 编码/解码工具
│   └── main.py
├── .gitignore
└── README.md
```

---

## 模块详情

### 1. AES 密钥生成器 `AES_key_generate1`

基于 HKDF（HMAC-based Extract-and-Expand Key Derivation Function）的 AES 密钥生成工具。

**核心功能：**

- 使用 `secrets` 模块生成高质量随机种子
- 通过 HKDF-SHA256 密钥派生函数派生密钥
- 支持三种密钥长度：**AES-128**、**AES-192**、**AES-256**

**运行：**

```bash
pip install cryptography
python AES_key_generate1/main.py
```

---

### 2. 密码学工具集 `Crypto1`

密码学算法实现与经典攻击演示，适用于 CTF 安全竞赛与密码学学习。

**核心功能：**

| 功能 | 说明 |
|------|------|
| RSA 加密/解密 | 基于 PyCryptodome 的 RSA 参数生成、加密与解密 |
| 扩展欧几里得算法 | 求解模逆元，支撑 RSA 共模攻击 |
| 共模攻击 | 当同一明文使用相同模数 n、不同公钥 e 加密时，无需私钥即可恢复明文 |
| 质因数分解 | 使用 SymPy 对大整数进行因数分解 |
| 共因子攻击 | 当两个 RSA 模数共享一个质因子时，通过 GCD 分解恢复 p、q |

**运行：**

```bash
pip install pycryptodome sympy
python Crypto1/main.py
python Crypto1/egcd.py
```

> 📖 详细说明见 [Crypto1/README_PROJECT.md](Crypto1/README_PROJECT.md)

---

### 3. k-匿名位置隐私保护 `k匿名位置隐私保护算法`

基于 DBSCAN 密度聚类的 k-匿名位置隐私保护算法，使用微软 Geolife GPS 轨迹数据集进行实验验证。

**核心功能：**

- **DBSCAN 密度聚类**：将空间邻近的位置点聚合为匿名集合
- **中心点泛化**：用簇中心坐标替代簇内所有点的真实位置
- **匿名区域可视化**：对比展示原始位置与匿名化结果，标注匿名区域覆盖人数

**算法流程：**

```
原始轨迹数据 → 随机采样 → DBSCAN 聚类 → 噪声点过滤 → 中心点泛化 → 匿名化结果
```

**运行：**

```bash
pip install numpy pandas matplotlib scikit-learn tqdm
python k匿名位置隐私保护算法/main.py
```

> ⚠️ 数据集需单独下载，详见 [k匿名位置隐私保护算法/README.md](k匿名位置隐私保护算法/README.md)

---

### 4. Netcat 网络工具 `netcat`

经典网络调试工具 **Netcat 1.11** 的 Windows NT 移植版本，由 Hobbit 原始编写、Weld Pond 移植至 Windows 平台。

**核心功能：**

- TCP/UDP 出站与入站连接
- 任意源端口与源地址绑定
- 内置端口扫描（支持随机化）
- 远程命令执行（`-e` 选项）
- Telnet 协议协商响应
- 后台无窗口运行模式（`-d` 选项）
- 十六进制数据转储

**编译：**

```bash
cd netcat
make          # 生成 nc.exe（需 MinGW i686-pc-mingw32-gcc 编译器）
```

**使用示例：**

```bash
# 连接远程主机
nc -v <host> <port>

# 监听端口
nc -l -p <port>

# 获取网页
nc -v www.example.com 80 < get.txt
```

---

### 5. 端口扫描器 `portScan`

功能丰富的端口扫描与 Web 指纹识别工具集，支持多种扫描模式与多线程加速。

**核心功能：**

| 文件 | 功能 |
|------|------|
| `PortScan.py` | TCP 全连接扫描、SYN 半开扫描、UDP 扫描、多线程并发 |
| `WebScan.py` | HTTP 指纹识别、SSL/TLS 证书分析 |

**扫描模式：**

| 模式 | 说明 | 权限要求 |
|------|------|:--------:|
| TCP Connect | 完整三次握手，最准确 | 普通 |
| TCP SYN | 半开扫描，更快更隐蔽 | ⚠️ root/管理员 |
| UDP | UDP 端口探测 | 普通 |

**运行：**

```bash
pip install scapy requests
# TCP 全连接扫描
python portScan/PortScan.py <target> -p 1-1024 -t connect

# SYN 扫描（需管理员权限）
sudo python portScan/PortScan.py <target> -p 1-1024 -t syn

# Web 指纹识别
python portScan/WebScan.py <target> -p 80 --ssl
```

> 📖 详细说明见 [portScan/README_PROJECT.md](portScan/README_PROJECT.md)

---

### 6. URL 编码工具 `URLencode`

URL 编码与解码工具，支持对包含特殊字符的 URL、Java 序列化数据等进行编码/解码处理。

**运行：**

```bash
python URLencode/main.py
```

---

## 技术栈

| 技术 | 用途 | 模块 |
|------|------|------|
| Python 3.8+ | 加密算法、扫描器、隐私保护 | AES_key_generate1, Crypto1, portScan, URLencode, k匿名 |
| C (MinGW) | Netcat 网络工具 | netcat |
| PyCryptodome | RSA 加密与数论运算 | Crypto1 |
| cryptography | HKDF 密钥派生 | AES_key_generate1 |
| scikit-learn | DBSCAN 密度聚类 | k匿名位置隐私保护算法 |
| Scapy | 网络数据包构造与发送 | portScan |
| SymPy | 大整数质因数分解 | Crypto1 |
| Matplotlib | 数据可视化 | k匿名位置隐私保护算法 |
| tqdm | 进度条 | k匿名位置隐私保护算法 |

---

## 快速开始

### 克隆仓库

```bash
git clone git@github.com:A-smile-cat/NetworkAndSecurity.git
cd NetworkAndSecurity
```

### Python 环境配置

建议使用虚拟环境：

```bash
python -m venv venv
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate       # Windows

# 安装全部 Python 依赖
pip install numpy pandas matplotlib scikit-learn tqdm pycryptodome sympy cryptography scapy requests
```

### 运行各模块

```bash
# AES 密钥生成
python AES_key_generate1/main.py

# 密码学工具
python Crypto1/main.py

# k-匿名位置隐私保护（需先准备数据集）
python k匿名位置隐私保护算法/main.py

# 端口扫描
python portScan/PortScan.py <target> -p 1-1024 -t connect

# Web 指纹识别
python portScan/WebScan.py <target> --ssl

# URL 编码
python URLencode/main.py
```

### 编译 Netcat

```bash
cd netcat
make    # 需 MinGW 编译环境
```

---

## 许可证

本项目仅供学习与研究使用。各子模块遵循其原始许可证：

- **Netcat**：遵循原始 [license.txt](netcat/license.txt)
- **Geolife 数据集**：遵循微软研究院使用协议
- **其余模块**：MIT License

---

## ⚠️ 免责声明

本仓库中的工具仅用于**合法的安全研究与教学目的**。端口扫描、网络监听等操作应在获得明确授权的前提下进行。使用者需自行承担因不当使用而产生的一切法律责任。

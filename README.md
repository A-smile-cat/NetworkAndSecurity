# Network & Security

网络安全与加密工具集，包含多个实用的网络安全工具和加密算法实现。

## 项目结构

```
NetworkAndSecurity/
├── AES_key_generate1/    # AES 密钥生成工具
├── Crypto1/               # 密码学算法实现 (RSA/ECC等)
├── URLencode/            # URL 编码/解码工具
├── netcat/               # Netcat 网络工具
└── portScan/             # 端口扫描工具
```

## 模块说明

### AES_key_generate1
AES 加密密钥生成工具，支持多种密钥长度和模式。

### Crypto1
基础密码学算法实现，包含：
- RSA 加密算法
- ECC (椭圆曲线密码学)
- Extended Euclidean Algorithm

### URLencode
URL 编码与解码工具，用于处理 URL 中的特殊字符。

### netcat
经典的网络工具 netcat，用于网络调试和端口扫描。支持：
- TCP/UDP 连接
- 端口监听
- 文件传输

### portScan
端口扫描工具，支持：
- TCP 端口扫描
- Web 端口探测

## 技术栈

- Python (密码学工具、端口扫描、URL编码)
- C (netcat)
- Makefile (编译构建)

## 使用方法

### Python 工具
```bash
# 端口扫描
python portScan/PortScan.py

# URL 编码
python URLencode/main.py

# AES 密钥生成
python AES_key_generate1/main.py

# 密码学工具
python Crypto1/main.py
```

### 编译 Netcat
```bash
cd netcat
make
```

## 许可证

本项目仅供学习和研究使用。
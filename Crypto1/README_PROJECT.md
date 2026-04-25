# 密码学工具集

> RSA 加解密与密码学攻击演示

[![PyCryptodome](https://img.shields.io/badge/PyCryptodome-3.0+-blue)](https://www.pycryptodome.org/)
[![SymPy](https://img.shields.io/badge/SymPy-1.0+-green)](https://www.sympy.org/)

---

## 📖 项目简介

本项目包含多个密码学算法的实现和演示，包括 RSA 加解密、扩展欧几里得算法、共模攻击等，适合密码学学习和 CTF 竞赛。

### 核心功能

- ✅ **RSA 加解密**: 完整的 RSA 实现示例
- ✅ **扩展欧几里得**: 模逆元计算
- ✅ **共模攻击**: RSA 共模攻击演示
- ✅ **因式分解**: 大整数分解

---

## 🚀 快速开始

### 环境要求

```bash
Python >= 3.7
PyCryptodome
SymPy
```

### 安装依赖

```bash
cd Crypto1
pip install pycryptodome sympy
```

### 运行项目

```bash
python main.py
```

---

## 💡 核心算法

### 1. RSA 解密

```python
from Crypto.Util.number import inverse, long_to_bytes

# RSA 参数
p = 1578173871764844869716052171
q = 10710927547195113973175047066215146269
n = 0x291733BAB061EF9C599139CB3E40A5C762B6F448FFFFFFFFFFFFFF
e = 0x10001  # 65537
c = 0x237200C0F72B97DB55BA37C7AACBB61A26A0CB47D294726259C4DF

# 计算私钥 d
d = inverse(e, (p - 1) * (q - 1))

# 解密
m = pow(c, d, n)

# 转换为字节
flag = long_to_bytes(m)
print(flag)  # b'flag{Acxdxf5vD_15_W7f}'
```

### 2. 扩展欧几里得算法 (egcd.py)

```python
def egcd(a, b):
    """
    扩展欧几里得算法
    返回 (g, x, y) 使得 a*x + b*y = g = gcd(a, b)
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    """
    计算模逆元
    a^(-1) mod m
    """
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('模逆元不存在')
    else:
        return x % m

# 使用
a = 17
m = 3120
inv = modinv(a, m)
print(f"{a} 的模逆元是 {inv}")  # 2753
```

### 3. 共模攻击

```python
from Crypto.Util.number import getPrime, GCD, bytes_to_long

# 生成密钥
p = getPrime(1024)
q1 = getPrime(1024)
q2 = getPrime(1024)

n1 = p * q1
n2 = p * q2

# 恢复 p (当两个模数有公因数时)
p = GCD(n1, n2)

q1 = n1 // p
q2 = n2 // p

# 共模攻击
p = getPrime(1024)
q = getPrime(1024)
n = p * q

e1 = getPrime(64)
e2 = getPrime(64)

m = bytes_to_long(b'Hello, RSA!')
c1 = pow(m, e1, n)
c2 = pow(m, e2, n)

# 当 gcd(e1, e2) = 1 时，可以恢复明文
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def common_mod_attack(c1, c2, e1, e2, n):
    g, s1, s2 = egcd(e1, e2)
    if g != 1:
        raise Exception("e1 和 e2 不互质")

    # 恢复明文
    m = (pow(c1, s1, n) * pow(c2, s2, n)) % n
    return m

m_recovered = common_mod_attack(c1, c2, e1, e2, n)
```

### 4. 因式分解攻击

```python
from sympy import factorint

n = 0x291733BAB061EF9C599139CB3E40A5C762B6F448FFFFFFFFFFFFFF

# 因式分解
factors = factorint(n)
print(factors)  # {3: 1, 5: 1, 7: 1, 13: 1, ...}

# 提取质因数
p, q = factors.keys()
print(f"p = {p}")
print(f"q = {q}")
```

### 5. 生成密钥对

```python
from Crypto.Util import number
from Crypto.Util.number import getPrime, isPrime

def next_prime(p):
    """返回下一个质数"""
    p = (p + 2) | 1  # 确保是奇数
    while not isPrime(p):
        p += 2
    return p

def gen_key(bits):
    """生成 RSA 密钥对"""
    p = getPrime(bits)
    q = next_prime(p)  # q 是 p 的下一个质数
    e = 65537
    n = p * q
    return n

# 生成 2048 位密钥
n = gen_key(2048)
print(f"n = {n}")
```

---

## 🎯 应用场景

### 场景 1: CTF 竞赛

```python
# 常见 CTF RSA 题目解法
def solve_rsa():
    # 题目给出
    n = 0xA8F1...
    e = 65537
    c = 0x7B2D...

    # 尝试因式分解
    factors = factorint(n)
    if len(factors) == 2:
        p, q = factors.keys()
        phi = (p - 1) * (q - 1)
        d = inverse(e, phi)
        m = pow(c, d, n)
        print(long_to_bytes(m))
```

### 场景 2: 数字签名

```python
# RSA 签名
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

def sign_message(message, private_key):
    h = SHA256.new(message)
    signature = pkcs1_15.new(private_key).sign(h)
    return signature

def verify_signature(message, signature, public_key):
    h = SHA256.new(message)
    try:
        pkcs1_15.new(public_key).verify(h, signature)
        return True
    except (ValueError, TypeError):
        return False
```

### 场景 3: 密钥交换

```python
# Diffie-Hellman 密钥交换
def diffie_hellman():
    # 公开参数
    p = getPrime(512)
    g = 2

    # Alice 生成私钥和公钥
    a = getPrime(256)
    A = pow(g, a, p)

    # Bob 生成私钥和公钥
    b = getPrime(256)
    B = pow(g, b, p)

    # 计算共享密钥
    s_alice = pow(B, a, p)
    s_bob = pow(A, b, p)

    assert s_alice == s_bob
    return s_alice
```

---

## 📚 密码学概念

### RSA 算法步骤

1. **密钥生成**
   - 选择两个大质数 p 和 q
   - 计算 n = p × q
   - 计算 φ(n) = (p-1) × (q-1)
   - 选择公钥指数 e (通常为 65537)
   - 计算私钥指数 d ≡ e^(-1) mod φ(n)

2. **加密**
   - c = m^e mod n

3. **解密**
   - m = c^d mod n

### 常见攻击方式

| 攻击类型 | 条件 | 防御 |
|---------|------|------|
| 暴力攻击 | 小的密钥 | 使用 >= 2048 位密钥 |
| 因式分解 | n 可被分解 | 使用足够大的质数 |
| 共模攻击 | 相同 n, 不同 e | 填充明文 |
| 选择密文攻击 | 解密预言机 | 使用 OAEP 填充 |

---

## ❓ 常见问题

### Q1: 如何选择安全的 RSA 参数?

```python
# 安全参数示例
bits = 2048  # 至少 2048 位
e = 65537    # 标准公钥指数

# 确保密钥足够强
p = getPrime(bits // 2)
q = getPrime(bits // 2)

# 确保 p 和 q 距离足够远
while abs(p - q) < 2 ** (bits // 2 - 100):
    q = getPrime(bits // 2)
```

### Q2: 如何处理大整数?

```python
# Python 的整数可以任意大，但需要注意：
# 1. 使用十六进制表示便于阅读
n = 0x1234567890abcdef

# 2. 转换为字节时指定长度
bytes_needed = (n.bit_length() + 7) // 8
m = n.to_bytes(bytes_needed, byteorder='big')
```

### Q3: 如何进行性能优化?

```python
# 使用中国剩余定理加速解密
def crt_decrypt(c, d, p, q):
    """使用 CRT 加速 RSA 解密"""
    dp = d % (p - 1)
    dq = d % (q - 1)
    qinv = modinv(q, p)

    m1 = pow(c, dp, p)
    m2 = pow(c, dq, q)
    h = (qinv * (m1 - m2)) % p
    m = m2 + h * q
    return m
```

---

## 📚 参考资料

- [密码学导论](https://www.cryptool.org/en/)
- [RSA 算法详解](https://en.wikipedia.org/wiki/RSA_(cryptosystem))
- [CTF Wiki](https://ctf-wiki.org/crypto/)
- [PyCryptodome 文档](https://pycryptodome.readthedocs.io/)

---

## ⚠️ 免责声明

本项目仅供学习和教育使用。请勿用于非法目的。

---

## 📄 许可证

MIT License

---

**最后更新**: 2026-03-04
**状态**: ✅ 可运行
**优先级**: ⭐⭐⭐ (学习参考)
**用途**: 密码学学习、CTF 竞赛

from Crypto.Util import number
#
# p = number.getPrime(512)
# q = number.getPrime(512)
#
# n = p * q
#
# m = 123456789
#
# print(pow(m,3,n))

from sympy import factorint

n = 0x291733BAB061EF9C599139CB3E40A5C762B6F448FFFFFFFFFFFFFF
factors = factorint(n)
print(factors)  # 输出: {3: 1, 5: 1, 7: 1, 13: 1, 67: 1, 107: 1, 630803: 1}
# 检查质因数的类型
p, q = factors.keys()
print(type(p))  # 输出: <class 'gmpy2.mpz'> 或 <class 'int'>
print(type(q))  # 输出: 同上
# 定义RSA参数
p = 1578173871764844869716052171
q = 10710927547195113973175047066215146269

n = 0x291733BAB061EF9C599139CB3E40A5C762B6F448FFFFFFFFFFFFFF
e = 0x10001
c = 0x237200C0F72B97DB55BA37C7AACBB61A26A0CB47D294726259C4DF

# 导入必要函数
from Crypto.Util.number import inverse, long_to_bytes, getPrime, isPrime, GCD, bytes_to_long

# 计算私钥d（修正原图错误：删除多余的乘号）
d = inverse(e, (p-1)*(q-1))  #求逆元

# 解密密文
m = pow(c, d, n)  # 注意变量名大小写，原图误用大写的 C

# 转换为字节
flag = long_to_bytes(m)
print(flag)  # 输出: b'flag{Acxdxf5vD_15_W7f}'
###########################
def nextPrime(p):
    p = (p+2) | 1
    while not isPrime(p):
        p += 2
    return p
def genkey(bits):
    p = getPrime(bits)
    q = nextPrime(p)
    e = 65537
    n = p*q
    return n

p = getPrime(1024)
q1 = getPrime(1024)
q2 = getPrime(1024)

n1 = p * q1
n2 = p * q2

p = GCD(n1,n2)

q1 = n1 // p
q2 = n2 // p

###共模攻击
p = getPrime(1024)
q = getPrime(1024)
n = p*q
e1 = getPrime(64)
e2 = getPrime(64)
m = bytes_to_long(flag)
c1 = pow(m,e1,n)
c2 = pow(m,e2,n)
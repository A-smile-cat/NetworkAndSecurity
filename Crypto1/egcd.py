from Crypto.Util.number import inverse, long_to_bytes, getPrime, isPrime, GCD, bytes_to_long
p = getPrime(1024)
q = getPrime(1024)
n = p*q
e1 = getPrime(64)
e2 = getPrime(64)

flag = b"flag{hello}"  # 必须是 bytes 类型
m = bytes_to_long(flag)
c1 = pow(m,e1,n)
c2 = pow(m,e2,n)

def egcd(a,b):
    u,u1 = 1,0
    v,v1 = 0,1
    while b:
        q,r = divmod(a,b)
        u,u1 = u1,u-q*u1
        v,v1 = v1,v-q*v1
        a,b = b,r
    return u,v,a

r,s,_ = egcd(e1,e2)
if r<0:
    r = -r
    c1 = inverse(c1,n)
else:
    s = -s
    c2 = inverse(c2,n)
m = pow(c1,r,n)*pow(c2,s,n) %n
print(long_to_bytes(m))
###
from Crypto.Util.number import inverse, long_to_bytes, getPrime, bytes_to_long

p = getPrime(1024)
q = getPrime(1024)
n = p * q
e1 = getPrime(64)
e2 = getPrime(64)

flag = b"flag{hello}"  # 必须是 bytes 类型
m = bytes_to_long(flag)

c1 = pow(m, e1, n)
c2 = pow(m, e2, n)

def egcd(a, b):
    u, u1 = 1, 0
    v, v1 = 0, 1
    while b:
        q, r = divmod(a, b)
        u, u1 = u1, u - q * u1
        v, v1 = v1, v - q * v1
        a, b = b, r
    return u, v, a

r, s, _ = egcd(e1, e2)
if r < 0:
    r = -r
    c1 = inverse(c1, n)
else:
    s = -s
    c2 = inverse(c2, n)

m_recovered = pow(c1, r, n) * pow(c2, s, n) % n
print(long_to_bytes(m_recovered))  # 输出: b'flag{hello}'
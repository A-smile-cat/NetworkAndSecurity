import hashlib
import secrets
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes


# 函数用于生成指定长度的AES密钥
def generate_aes_key(random_bytes, key_length_bits):
    # 使用HKDF进行密钥派生
    salt = secrets.token_bytes(16)  # 可选，增加额外的熵
    info = b'handshake data'  # 可选，上下文信息

    kdf = HKDF(
        algorithm=hashes.SHA256(),
        length=key_length_bits // 8,
        salt=salt,
        info=info,
    )

    return kdf.derive(random_bytes)


# 生成三个随机数
random_num_1 = secrets.randbits(16).to_bytes(2, byteorder='big')  # 2字节
random_num_2 = secrets.randbits(16).to_bytes(2, byteorder='big')  # 2字节
random_num_3 = secrets.randbits(22).to_bytes(3, byteorder='big')  # 22位，填充到3字节

# 将三个随机数组合并进行哈希以确保即使知道两个随机数也无法还原原始密钥
combined_random = random_num_1 + random_num_2 + random_num_3
hashed_combined_random = hashlib.sha256(combined_random).digest()

# 生成不同长度的AES密钥
aes_128_key = generate_aes_key(hashed_combined_random, 128)
aes_192_key = generate_aes_key(hashed_combined_random, 192)
aes_256_key = generate_aes_key(hashed_combined_random, 256)

# 打印生成的AES密钥（在实际应用中应避免打印或暴露密钥）
print("AES-128 Key:", aes_128_key.hex())
print("AES-192 Key:", aes_192_key.hex())
print("AES-256 Key:", aes_256_key.hex())

from scapy.all import *
from scapy.layers.http import HTTP, HTTPRequest
import argparse

from scapy.layers.inet import IP, TCP
from scapy.layers.tls.extensions import TLS_Ext_ServerName, TLS_Ext_SupportedGroups, ServerName, \
    TLS_Ext_SupportedVersions, TLS_Ext_SignatureAlgorithms
from scapy.layers.tls.handshake import TLSClientHello
from scapy.layers.tls.record import TLS,TLS13ClientHello,TLS13ServerHello
import requests

def http_fingerprint(target, port=80):
    print(f"[*] 开始对 {target}:{port} 进行HTTP指纹识别...")

    url = f"http://{target}:{port}"
    try:
        response = requests.get(url, timeout=5)
        print("\n[+] HTTP指纹识别结果:")
        print(f"  HTTP版本: HTTP/1.1")  # 假设服务器使用 HTTP/1.1
        print(f"  状态码: {response.status_code}")
        print(f"  服务器类型: {response.headers.get('Server', '未公开')}")
        print(f"  后端技术: {response.headers.get('X-Powered-By', '未公开')}")
        print(f"  使用Cookie: {'是' if 'Set-Cookie' in response.headers else '否'}")
    except requests.exceptions.RequestException as e:
        print(f"[-] 无法连接到目标: {e}")

def ssl_fingerprint(target, port=443):
    """
    执行SSL/TLS指纹识别
    """
    print(f"\n[*] 开始对 {target}:{port} 进行SSL/TLS指纹识别...")

    # 发送ClientHello
    pkt = IP(dst=target) / TCP(dport=port, flags="S")
    resp = sr1(pkt, timeout=2, verbose=0)

    if not resp:
        print("[-] 目标无响应")
        return

    # 建立TCP连接
    ack_pkt = IP(dst=target) / TCP(dport=port, flags="A", seq=resp.ack, ack=resp.seq + 1)
    send(ack_pkt, verbose=0)

    # 发送TLS ClientHello
    client_hello = IP(dst=target) / TCP(dport=port, flags="PA", seq=ack_pkt.seq, ack=ack_pkt.ack) / TLS(
        version=0x0303) / TLS13ClientHello()

    resp = sr1(client_hello, timeout=5, verbose=0)

    if not resp:
        print("[-] 未收到TLS响应")
        return

    # 分析响应
    print("\n[+] SSL/TLS指纹识别结果:")
    if resp.haslayer(TLS):
        tls_layer = resp.getlayer(TLS)
        print(f"  TLS版本: {hex(tls_layer.version)}")

        if tls_layer.haslayer("TLSHandshakes"):
            handshakes = tls_layer.getlayer("TLSHandshakes")
            if handshakes.haslayer("TLpySServerHello"):
                server_hello = handshakes.getlayer("TLSServerHello")
                print(f"  支持的加密套件: {server_hello.cipher_suites}")

    else:
        print("  响应中未检测到TLS层")



def main():
    parser = argparse.ArgumentParser(description="网站指纹识别工具")
    parser.add_argument("target", help="目标网站域名或IP")
    parser.add_argument("-p", "--port", type=int, default=80, help="目标端口 (默认: 80)")
    parser.add_argument("--ssl", action="store_true", help="执行SSL/TLS指纹识别")

    args = parser.parse_args()

    # HTTP指纹识别
    http_fingerprint(args.target, args.port)

    # 如果指定了SSL选项或端口是443，执行SSL指纹识别
    if args.ssl or args.port == 443:
        ssl_fingerprint(args.target, args.port)


if __name__ == "__main__":
    main()
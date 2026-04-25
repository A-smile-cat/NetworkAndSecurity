#!/usr/bin/env python3
from scapy.all import *
import argparse
import ipaddress
import time
import sys
from concurrent.futures import ThreadPoolExecutor

# 禁用Scapy的冗余输出
from scapy.layers.inet import IP,TCP,UDP,ICMP

conf.verb = 0

def tcp_connect_scan(target, port, timeout=10):
    """
    TCP全连接扫描 - 与目标端口建立完整的三次握手
    参数:
        target (str): 目标IP地址或域名
        port (int): 要扫描的目标端口号
        timeout (int): 连接超时时间（秒），默认10秒
    返回值:
        bool: 端口开放返回True，否则返回False
    """

    # 创建TCP套接字
    # AF_INET 表示IPv4地址族
    # SOCK_STREAM 表示TCP协议
    try:
        connect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # 设置连接超时时间
        # 超过指定时间未建立连接则放弃
        connect.settimeout(timeout)

        # 尝试连接目标端口
        # connect_ex()返回错误码（0表示成功）
        # 相比connect()不会抛出异常，更适合扫描场景
        rescode = connect.connect_ex((target, port))

        # 关闭连接（优雅断开）
        # shutdown(2)表示同时关闭读写通道
        if rescode == 0:  # 连接成功
            connect.shutdown(2)  # 先关闭连接
            connect.close()  # 释放套接字资源
            return True
        return False

    except socket.timeout:
        # 连接超时处理
        print(f"连接{target}:{port}超时（{timeout}s）")
        return False

    except socket.error as e:
        # 其他socket异常处理
        print(f"连接{target}:{port}发生错误: {str(e)}")
        return False

    except Exception as e:
        # 捕获其他所有异常
        print(f"未知错误: {str(e)}")
        return False


def tcp_syn_scan(target, port, timeout=1):
    """
    TCP SYN扫描 (半开扫描)
    参数:
        target (str): 目标IP地址
        port (int): 要扫描的目标端口
        timeout (int): 等待响应超时时间(秒)，默认1秒
    返回值:
        bool: 端口开放返回True，否则返回False
    """

    try:
        # 构造SYN数据包
        # IP层: 设置目标地址(dst)
        # TCP层: 设置目标端口(dport)和SYN标志(flags='S')
        syn_pkt = IP(dst=target) / TCP(dport=port, flags='S')

        # 发送数据包并等待单个响应(sr1)
        # timeout参数控制等待时间
        resp = sr1(syn_pkt, timeout=timeout)

        # 无响应情况处理
        if resp is None:
            return False  # 可能被防火墙过滤或网络问题

        # 检查响应包是否包含TCP层
        if resp.haslayer(TCP):
            # 获取TCP标志位
            tcp_flags = resp.getlayer(TCP).flags

            # 0x12 = SYN-ACK (二进制00010010)
            if tcp_flags == 0x12:  # 端口开放
                # 发送RST包终止连接(避免建立完整连接)
                rst_pkt = IP(dst=target) / TCP(dport=port, flags='R')
                send(rst_pkt, timeout=timeout)
                return True

            # 0x14 = RST-ACK (二进制00010100)
            elif tcp_flags == 0x14:  # 端口关闭
                return False

        return False  # 其他情况视为关闭

    except Exception as e:
        print(f"TCP SYN扫描错误: {e}")
        return False


def tcp_fin_scan(target, port, timeout=1):
    """
    TCP FIN扫描 (隐蔽端口扫描技术)
    参数:
        target (str): 目标IP地址
        port (int): 要扫描的目标端口
        timeout (int): 等待响应超时时间(秒)，默认1秒
    返回值:
        bool:
            True - 端口可能开放(无响应)或被过滤
            False - 端口明确关闭(收到RST)
    """

    try:
        # 构造FIN数据包
        # IP层: 设置目标地址(dst)
        # TCP层: 设置目标端口(dport)和FIN标志(flags='F')
        # flags='F'表示FIN=1(二进制00000001)
        fin_pkt = IP(dst=target) / TCP(dport=port, flags='F')

        # 发送数据包并等待单个响应(sr1)
        # verbose=0关闭scapy默认输出
        resp = sr1(fin_pkt, timeout=timeout, verbose=0)

        # 无响应情况处理
        if resp is None:
            return True  # 可能开放或被过滤

        # 检查响应包是否包含TCP层
        if resp.haslayer(TCP):
            # 获取TCP标志位
            tcp_flags = resp.getlayer(TCP).flags

            # 0x14 = RST-ACK (二进制00010100)
            if tcp_flags == 0x14:  # 收到RST表示端口关闭
                return False

        return True  # 其他情况视为可能开放

    except Exception as e:
        print(f"[!] TCP FIN扫描错误: {str(e)}")
        return False


def tcp_null_scan(target, port, timeout=1):
    """
    TCP NULL扫描 (全零标志位扫描)
    参数:
        target (str): 目标IP地址或域名
        port (int): 要扫描的目标端口(1-65535)
        timeout (int): 等待响应超时时间(秒)，默认1秒
    返回值:
        bool:
            True - 端口可能开放(无响应)或被过滤
            False - 端口明确关闭(收到RST)
    """

    try:
        # 构造NULL数据包
        # IP层: 设置目标地址(dst)
        # TCP层:
        #   - dport: 目标端口
        #   - flags='': 所有标志位清零(0x00)
        null_pkt = IP(dst=target) / TCP(dport=port, flags='')

        # 发送并等待响应
        # sr1()发送接收单包，timeout控制等待时间
        # verbose=0关闭scapy默认输出
        resp = sr1(null_pkt, timeout=timeout, verbose=0)

        # 响应分析
        if resp is None:
            # 无响应情况
            return True  # 可能开放或被过滤

        if resp.haslayer(TCP):
            # 检查TCP层标志位
            # 0x14 = RST-ACK (二进制00010100)
            if resp.getlayer(TCP).flags == 0x14:
                return False  # 收到RST表示端口关闭

        return True  # 其他情况视为可能开放

    except Exception as e:
        # 异常处理
        print(f"[!] TCP NULL扫描错误: {str(e)}")
        return False


def tcp_xmas_scan(target, port, timeout=1):
    """
    TCP XMAS扫描 (圣诞树扫描)
    参数:
        target (str): 目标IP地址
        port (int): 要扫描的目标端口(1-65535)
        timeout (int): 等待响应超时时间(秒)，默认1秒
    返回值:
        bool:
            True - 端口可能开放(无响应)或被过滤
            False - 端口明确关闭(收到RST)
    """

    try:
        # 构造XMAS数据包
        # IP层: 设置目标地址(dst)
        # TCP层:
        #   - dport: 目标端口
        #   - flags='FPU':
        #     F=FIN(0x01), P=PSH(0x08), U=URG(0x20)
        #     组合后flags=0x29(二进制00101001)
        xmas_pkt = IP(dst=target) / TCP(dport=port, flags='FPU')

        # 发送并等待响应
        # sr1()发送接收单包，timeout控制等待时间
        # verbose=0关闭scapy默认输出
        resp = sr1(xmas_pkt, timeout=timeout, verbose=0)

        # 响应分析
        if resp is None:
            # 无响应情况
            return True  # 可能开放或被过滤

        if resp.haslayer(TCP):
            # 检查TCP层标志位
            # 0x14 = RST-ACK (二进制00010100)
            if resp.getlayer(TCP).flags == 0x14:
                return False  # 收到RST表示端口关闭

        return True  # 其他情况视为可能开放

    except Exception as e:
        # 异常处理
        print(f"[!] TCP XMAS扫描错误: {str(e)}")
        return False


def scan_port(target, port, scan_type):
    """根据扫描类型调用相应的扫描函数"""
    if scan_type == 'tcp_connect':
        return ('TCP', port, tcp_connect_scan(target, port))
    elif scan_type == 'tcp_syn':
        return ('TCP', port, tcp_syn_scan(target, port))
    elif scan_type == 'tcp_fin':
        return ('TCP', port, tcp_fin_scan(target, port))
    elif scan_type == 'tcp_null':
        return ('TCP', port, tcp_null_scan(target, port))
    elif scan_type == 'tcp_xmas':
        return ('TCP', port, tcp_xmas_scan(target, port))
    else:
        return (None, port, None)


def port_scan(target, ports, scan_type='tcp_syn'):
    """
    单线程执行端口扫描
    :param target: 目标IP或主机名
    :param ports: 要扫描的端口列表
    :param scan_type: 扫描类型
    :return: 开放端口列表
    """
    open_ports = []

    print(f"\n[*] 开始对 {target} 进行 {scan_type} 扫描...")
    start_time = time.time()

    # 单线程顺序扫描每个端口
    for port in ports:
        protocol, port, status = scan_port(target, port, scan_type)

        if status is True or status == "open|filtered" or status == "unfiltered":
            print(f"[+] {protocol} 端口 {port} 开放")
            open_ports.append(port)
        elif status is False or status == "filtered":
            pass
            # print(f"[-] {protocol} 端口 {port} 关闭")
        else:
            print(f"[?] {protocol} 端口 {port} 状态未知: {status}")

    elapsed_time = time.time() - start_time
    print(f"\n[*] 扫描完成! 发现 {len(open_ports)} 个开放端口:")
    print(open_ports)
    print(f"[*] 耗时: {elapsed_time:.2f} 秒")
    return open_ports

def parse_ports(port_str):
    """解析端口范围字符串，如 '1-100' 或 '22,80,443'"""
    ports = []
    parts = port_str.split(',')

    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            ports.extend(range(start, end + 1))
        else:
            ports.append(int(part))

    return ports


def interactive_mode():
    """交互式模式"""
    print("\n=== 端口扫描（交互模式） ===")

    # 获取目标
    target = input("输入目标IP或主机名: ").strip()
    try:
        # 验证目标IP
        ipaddress.ip_address(target)
    except ValueError:
        try:
            # 尝试解析主机名
            target = socket.gethostbyname(target)
        except socket.gaierror:
            print("错误: 无效的目标地址或主机名")
            return

    # 获取端口范围
    port_str = input("输入要扫描的端口(如 1-100 或 22,80,443;默认1-65535): ").strip()
    if port_str == "":
        port_str = "1-65535"
    try:
        ports = parse_ports(port_str)
    except ValueError:
        print("错误: 无效的端口格式")
        return

    # 选择扫描类型
    print("\n选择扫描类型（默认1）:")
    print("1. TCP SYN扫描 (半开扫描, 速度快, 较隐蔽)")
    print("2. TCP Connect扫描 (全连接, 准确但慢)")
    print("3. TCP FIN扫描 (隐蔽)")
    print("4. TCP NULL扫描 (高度隐蔽)")
    print("5. TCP XMAS扫描 (隐蔽)")


    choice = input("输入选择(1-5): ").strip()
    scan_types = {
        '1': 'tcp_syn',
        '2': 'tcp_connect',
        '3': 'tcp_fin',
        '4': 'tcp_null',
        '5': 'tcp_xmas',
    }

    if choice == "":
        choice = '1'

    if choice not in scan_types:
        print("错误: 无效的选择")
        return

    # 执行扫描
    port_scan(target, ports, scan_types[choice])


def main():
    """主函数，处理命令行参数"""
    parser = argparse.ArgumentParser(description='综合端口扫描工具')
    parser.add_argument('target', help='目标IP或主机名', nargs='?')
    parser.add_argument('-p', '--ports', help='要扫描的端口范围，如 1-100 或 22,80,443',default='1-65535')
    parser.add_argument('-t', '--type', help='扫描类型', choices=[
        'tcp_syn', 'tcp_connect', 'tcp_fin',
        'tcp_null', 'tcp_xmas'
    ], default='tcp_syn')

    args = parser.parse_args()

    if not args.target:
        # 如果没有提供命令行参数，进入交互模式
        interactive_mode()
    else:
        # 验证目标IP
        try:
            ipaddress.ip_address(args.target)
        except ValueError:
            try:
                # 尝试解析主机名
                args.target = socket.gethostbyname(args.target)
            except socket.gaierror:
                print("错误: 无效的目标地址或主机名")
                sys.exit(1)

        # 解析端口
        if not args.ports:
            print("错误: 必须指定端口范围")
            parser.print_help()
            sys.exit(1)

        try:
            ports = parse_ports(args.ports)
        except ValueError:
            print("错误: 无效的端口格式")
            sys.exit(1)

        # 执行扫描
        port_scan(args.target, ports, args.type)


if __name__ == '__main__':
    main()
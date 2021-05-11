# coding:utf-8

import os
import socket
import dns.resolver
import configparser
import subprocess
import re
from function.logs.logings import check_logs
from function.app_class import PyWinAuto
log = check_logs()


def check_dir():
    """
    :return: install path
    """
    vpm_dir = "C:/Program Files (x86)/SecoClient/SecoClient.exe"
    agent_dir = "c:/Windows/Agt3Tool.exe"
    sdc_dir = "C:/Program Files/CnSinDa/SDC4/ClientL/x64/CliLSvc.exe"
    p1 = os.path.exists(vpm_dir)
    p2 = os.path.exists(agent_dir)
    p3 = os.path.exists(sdc_dir)
    return p1, p2, p3


def check_path():
    """检查安装目录，如果不存在就新建"""
    path = os.getcwd()
    if path == './':
        pass
    else:
        if os.path.isdir('function'):
            if os.path.isdir('install'):
                pass
            else:
                os.makedirs('install')
        else:
            os.chdir('./')
            if os.path.isdir('install'):
                pass
            else:
                os.makedirs('install')


def check_setup():
    """检查安装目录下的安装包是否存在"""
    path = os.getcwd()
    if path == '../':
        pass
    else:
        if os.path.isfile('install/agent4.exe') and os.path.isfile('install/secoclient.exe')\
                and os.path.isfile('install/SetupClientLV4.exe'):
            return 0
        else:
            return 1


def get_ping_result(send_cmd):
    p = subprocess.Popen(send_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, shell=True)
    out = p.stdout.read().decode('gbk')

    reg_receive = '已接收 = \d'
    match_receive = re.search(reg_receive, out)

    receive_count = 0

    if match_receive:
        receive_count = int(match_receive.group()[6:])

    if receive_count > 0:  # 接受到的反馈大于0，表示网络通
        reg_min_time = '最短 = \d+ms'
        reg_max_time = '最长 = \d+ms'
        reg_avg_time = '平均 = \d+ms'

        match_min_time = re.search(reg_min_time, out)
        min_time = int(match_min_time.group()[5:-2])

        match_max_time = re.search(reg_max_time, out)
        max_time = int(match_max_time.group()[5:-2])

        match_avg_time = re.search(reg_avg_time, out)
        avg_time = int(match_avg_time.group()[5:-2])

        return [receive_count, min_time, max_time, avg_time]
    else:
        # print('网络不通，目标服务器不可达！')
        log.warning("Network host not found")
        return [0, 9999, 9999, 9999]


def check_vpn():
    """
    检查vpn配置、服务状态
    GatewayAddress:网关地址
    GatewayPort：网关端口
    TunnelMode：隧道模式、0=自动 1=tcp 2=udp
    """
    pid_name = "SecoClient.exe"
    path = os.environ['APPDATA']
    # 检查配置问题
    log.info("---" * 16 + "vpn检查" + "---" * 16)
    if os.path.isdir(path + r"/SecoClient/config"):
        log.info("Configuration file exists")
        path = os.environ['APPDATA']
        tes = path + "/SecoClient/config/"
        for i in os.listdir(tes):
            os.chdir(tes)
            cnf = configparser.RawConfigParser()
            cnf.read(i)
            get_ipaddr = cnf.get('GLOBAL', 'GatewayAddress')
            get_port = cnf.get('GLOBAL', 'GatewayPort')
            get_tunnel = cnf.get('GLOBAL', 'TunnelMode')
            ip = "121.33.243.38"
            port = "8440"
            if get_ipaddr == ip:
                log.info('gateway address configuration ' + get_ipaddr)
            else:
                log.warning("Incorrect gateway address configuration! " + get_ipaddr)
            if get_port == port:
                log.info('Port configuration ' + port)
                log.info('TunnelMode configuating ' + get_tunnel)
            else:
                log.warning('Incorrect Port configuration ' + port)
        # 检查进程
        if PyWinAuto.get_pid(pid_name) is None:
            log.info('SECO  process is not running')
            test_ip = get_ping_result("192.168.0.1")
            # print(loging.log_warn("get_ping_result"), test_ip)
            log.warning("get_ping_result")
            log.info(test_ip)
        else:
            log.info('SECO Process running')
            # 获取虚拟IP
            ipv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            ipv.connect(('192.168.0.1', 80))
            vip = ipv.getsockname()[0]
            log.info("Virtual IP address: " + vip)
        # 获取用户名和IP
        local_name = socket.gethostname()
        # 获取本机ip
        ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip.connect(('114.114.114.114', 80))
        ip2 = ip.getsockname()[0]
        log.info("Local_name: " + local_name + ' ' + "local_ipaddress: " + ip2)

    else:
        log.warning("The configuration file does not exist")


def check_agent():
    # 检查是否安装准入客户端
    log.info("---" * 16 + "准入检查" + "---" * 16)
    if os.path.exists('c:\Windows\Agt3Tool.exe'):
        log.info("IPG-guard in installd")
    else:
        log.warning("IPG-guard not installd")


def check_sdc():
    # 检查沙盒安装情况
    log.info("---" * 16 + "沙盒检查" + "---" * 16)
    sdc_pid = 'CliLTrayEx.exe'
    if os.path.exists('C:\Program Files\CnSinDa\SDC4'):
        log.info("SDC4 file exists")
        # 检查服务运行状态
        if PyWinAuto.get_pid(sdc_pid) is None:
            log.warning("SDC The process is not running")
        else:
            log.info("SDC Process running")
            # 检查服务器IP连通性
            sdc_server = get_ping_result('ping 192.168.0.209')
            if sdc_server[0] > 3:
                log.info("SDC Server connected successfully")
            else:
                log.warning("SDC Server connection failed")
            # 检查sdc与服务器TCP、UDP
            pass
            # 检查sdc在线情况
            pass
    else:
        log.warning("The SDC4 file does not exist")


def check_dns():
    # 检查dns解析情况
    log.info("---" * 16 + "dns检查" + "---" * 16)
    domain = "oa.zlgmcu.com"
    try:
        a = dns.resolver.query(domain)
        for i in a.response.answer:
            for j in i.items:

                log.info("Domain name address resolved successfully ")
    except:
        log.warning("Domain name address resolution failed")


# if __name__ == '__main__':
#     abc = check_setup()
#     print(abc)
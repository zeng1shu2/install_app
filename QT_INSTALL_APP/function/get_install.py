import os
import requests
import threading


def get_vpn():
    vpn_url = 'http://doc.zlg.cn/vpn/secoclient-win-64-7.0.2.26.exe'
    j_path = './install/secoclient.exe'
    return vpn_url, j_path


def get_agent():
    agent_url = 'http://doc.zlg.cn/vpn/agent4.exe'
    j_path = './install/agent4.exe'
    return agent_url, j_path


def get_sdc():
    sdc_url = 'http://doc.zlg.cn/vpn/SetupClientLV4.exe'
    j_path = './install/SetupClientLV4.exe'
    return sdc_url, j_path


def handler(start, end, url, filename):
    headers = {'Range': 'bytes=%d-%d' % (start, end)}
    r = requests.get(url, headers=headers, stream=True, timeout=5)
    # 写入文件对应位置
    with open(filename, "r+b") as fp:
        fp.seek(start)
        var = fp.tell()
        fp.write(r.content)


def download_file(urls, file_name, num_thread=10):
    r = requests.head(urls)
    try:
        file_name1 = urls.split('/')[-1]
        file_size = int(r.headers['content-length'])
    except:
        print("检查URL，或不支持对线程下载")
        return
    #  创建一个和要下载文件一样大小的文件
    fp = open(file_name, "wb")
    fp.truncate(file_size)
    fp.close()
    # 启动多线程写文件
    part = file_size // num_thread
    # 如果不能整除，最后一块应该多几个字节
    for i in range(num_thread):
        starts = part * i
        if i == num_thread - 1:   # 最后一块
            ends = file_size
        else:
            ends = starts + part
        t = threading.Thread(target=handler, kwargs={'start': starts, 'end': ends, 'url': urls, 'filename': file_name})
        t.setDaemon(True)
        t.start()
    # 等待所有线程下载完成
    main_thread = threading.current_thread()
    for t in threading.enumerate():
        if t is main_thread:
            continue
        t.join()
    print('%s 下载完成' % file_name1)


def vpn():
    download_file(get_vpn()[0], get_vpn()[1])


def agent():
    download_file(get_agent()[0], get_agent()[1])


def sdc():
    download_file(get_sdc()[0], get_sdc()[1])

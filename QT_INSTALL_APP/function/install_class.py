# coding:utf-8

import os
import json
from time import sleep
from function.Erroe import app_error
from function.configs import path
from function.app_class import PyWinAuto
from function import check_config
from ctypes import *
from function.configs import values


class Installer(object):
    def __init__(self):
        app = PyWinAuto()
        self.app = app
        self.lock_ = windll.LoadLibrary('user32.dll')

    def lock(self):
        """锁定鼠标键盘"""
        self.lock_.BlockInput(True)

    def unlock(self):
        """解锁鼠标键盘"""
        self.lock_.BlockInput(False)

    @staticmethod
    def open_json():
        p_dir = path.path()
        file_path = 'values.json'
        file_path = os.path.join(p_dir, file_path)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                j_data = f.read()
                j_data = json.loads(j_data)
                return j_data
        else:
            raise app_error.FileErr('读取的文件不存在')

    @staticmethod
    def open_config():
        file_path = values.config_info
        return file_path

    def agent(self):
        app = self.app
        j_data = Installer.open_config()
        j_data = j_data['agent']
        windows_title = j_data.get('windows_title')
        try:
            _isdir = os.path.abspath('./install')
            # print(_isdir)
            app_path = _isdir+'\\Agent4.exe'
            if os.path.exists(app_path):
                self.lock()
                app.run(app_path)
                # 调用子进程
                if PyWinAuto.get_pid(j_data['name_process']) is None:
                    num = 0
                    while num < 60:
                        if PyWinAuto.get_pid(j_data['name_process']) is None:
                            num += 1
                            # print('获取进程号中', num)
                            sleep(1)
                            continue
                        else:
                            break
                    if PyWinAuto.get_pid(j_data['name_process']) is not None:
                        windows_process = PyWinAuto.get_pid(j_data['name_process'])
                        app.connect(windows_process)
                        app.next(windows_title, j_data['windows_next'])
                        app.accept(windows_title, j_data['windows_accept'])
                        app.wait_time(windows_title, j_data['windows_cpl'])
                        app.query_action(windows_title, j_data['windows_un1'])
                        app.finish(windows_title, j_data['windows_cpl'])
                        self.unlock()
                    else:
                        print('尝试了60秒钟任然无法获取启动进程号，将退出程序')
                else:
                    windows_process = PyWinAuto.get_pid(j_data['name_process'])
                    app.connect(windows_process)
                    app.next(windows_title, j_data['windows_next'])
                    app.accept(windows_title, j_data['windows_accept'])
                    app.wait_time(windows_title, j_data['windows_cpl'])
                    app.query_action(windows_title, j_data['windows_un1'])
                    app.finish(windows_title, j_data['windows_cpl'])
                    self.unlock()
            else:
                raise app_error.FileErr('文件错误，文件目录不存在')
        except app_error.InstallErr as e:
            print(e.message)

    def vpn(self):
        app = self.app
        j_data = Installer.open_config()
        j_data = j_data['vpn']
        windows_title = j_data.get('windows_title')
        try:
            _isdir = os.path.abspath('./install')
            app_path = _isdir+'/secoclient.exe'
            if os.path.exists(app_path):
                if os.path.exists(j_data.get('arg')):
                    # 程序已经安装不在启动安装
                    print("SecoClient Exists")
                else:
                    self.lock()
                    app.run(app_path)
                    app.next(windows_title, j_data['windows_next'])
                    app.accept(windows_title, j_data['windows_accept'])
                    if PyWinAuto.get_pid(j_data['name_process']) is None:
                        i = 0
                        while i < 10:
                            i += 1
                            sleep(1)
                            if PyWinAuto.get_pid(j_data['name_process']) is not None:
                                print("检测到windows安全弹窗,准备安装虚拟驱动。")
                                break
                            else:
                                pass
                        if PyWinAuto.get_pid(j_data['name_process']) is not None:
                            windows_process = PyWinAuto.get_pid(j_data['name_process'])
                            app.connect(windows_process)
                            app.windows_security_setup(j_data['windows_title_secc'], j_data['windows_secc'])
                            windows_process1 = PyWinAuto.get_pid(j_data['name_process1'])
                            app.connect(windows_process1)
                            app.wait_time(windows_title, j_data['windows_cpl'])
                            app.finish(windows_title, j_data['windows_cpl'])
                            self.unlock()
                        else:
                            app.wait_time(windows_title, j_data['windows_cpl'])
                            app.finish(windows_title, j_data['windows_cpl'])
                            self.unlock()
                    else:
                        app.wait_time(windows_title, j_data['windows_cpl'])
                        app.finish(windows_title, j_data['windows_cpl'])
                        self.unlock()
            else:
                print('文件错误，文件目录不存在')
                raise app_error.FileErr('文件错误，文件目录不存在')
        except app_error.InstallErr as e:
            print(e.message)

    def sdc(self):
        app = self.app
        j_data = Installer.open_config()
        j_data = j_data['sdc']
        windows_title = j_data.get('windows_title')
        try:
            _isdir = os.path.abspath('./install')
            app_path = _isdir+'/SetupClientLV4.exe'
            if os.path.exists(app_path):
                if os.path.exists(j_data.get('arg')):
                    # 程序已经安装不在启动安装
                    print('SDC Exists')
                else:
                    self.lock()
                    app.run(app_path)
                    sleep(1)
                    windows_process = PyWinAuto.get_pid(j_data['name_process'])
                    app.connect(windows_process)
                    app.query_action(j_data['windows_un'], j_data['windows_un1'])
                    sleep(1)
                    app.next(windows_title, j_data['windows_next'])
                    app.accept(windows_title, j_data['windows_accept'])
                    app.next(windows_title, j_data['windows_next'])
                    app.send(windows_title, j_data['windows_edit'], j_data['windows_host'])
                    sleep(1)
                    # 检查服务器连接性
                    result = check_config.get_ping_result('ping  -n 2 192.168.0.209')
                    sleep(1)
                    if result[1] >= 0:
                        app.next(windows_title, j_data['windows_next'])
                        app.next(windows_title, j_data['windows_next'])
                        app.next(windows_title, j_data['windows_next'])
                        app.accept(windows_title, j_data['windows_setup'])
                        app.wait_time(windows_title, j_data['windows_cpl'])
                        app.accept(windows_title, j_data['windows_un2'])
                        sleep(1)
                        app.finish(windows_title, j_data['windows_cpl'])
                        self.unlock()
                    else:
                        app.next(windows_title, j_data['windows_next'])
                        app.wait_time(j_data['windows_un'], j_data['windows_un3'])
                        app.query_action(j_data['windows_un'], j_data['windows_un3'])
                        app.next(windows_title, j_data['windows_next'])
                        app.next(windows_title, j_data['windows_next'])
                        app.accept(windows_title, j_data['windows_setup'])
                        app.wait_time(windows_title, j_data['windows_cpl'])
                        app.accept(windows_title, j_data['windows_un2'])
                        sleep(1)
                        app.finish(windows_title, j_data['windows_cpl'])
                        self.unlock()
            else:
                raise app_error.FileErr('文件错误，文件目录不存在')
        except app_error.InstallErr as e:
            print(e.message)





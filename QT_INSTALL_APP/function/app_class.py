# coding:utf-8
from pywinauto import application
from time import sleep
import psutil


class PyWinAuto(object):
    """
    """
    def __init__(self):
        """初始化APP"""
        self.app = application.Application()

    @staticmethod
    def get_pid(name):
        """:根据进程名获取pid"""
        for proc in psutil.process_iter():
            if proc.name() == name:
                return proc.pid

    def run(self, app_path):
        """:启动APP"""
        self.app.start(app_path, timeout=1, retry_interval=0.5)
        sleep(1)

    def identifier(self, title):
        """:打印标识符"""
        self.app[title].print_control_identifiers()

    def connect(self, process):
        """:连接APP"""
        self.app.connect(process=process)
        sleep(1)

    def close(self, name):
        """:关闭APP"""
        self.app[name].Close()
        sleep(1)

    def send(self, windows_title, edit, value):
        """:键入value"""
        self.app[windows_title].child_window(class_name=edit).type_keys(value, with_spaces=True)

    def query_windows(self, title, value):
        """:查询弹出窗口"""
        self.app[title].child_window(title=value).wait('enabled', timeout=2, retry_interval=0.5)

    def query_action(self, title, value):
        """查询到安装后双击点否"""
        self.app[title].child_window(title=value).click_input()

    def wait_time(self, title, value):
        """等待时间,超时300秒，1秒查询一次"""
        self.app[title].child_window(title=value).wait('enabled', timeout=300, retry_interval=2)

    def next(self, title, value):
        """下一步"""
        self.app[title].child_window(title=value).click_input()

    def accept(self, title, value):
        """接受、安装"""
        self.app[title].child_window(title=value).click_input()

    def finish(self, title, value):
        """完成"""
        self.app[title].child_window(title=value).click_input()

    def query_windows_security(self, process):
        """查询弹出安全认证"""
        self.app.connect(process=process).wait('enabled', timeout=30, retry_interval=0.5)
        sleep(2)

    def windows_security_setup(self, title, value):
        """:security安全驱动安装"""
        self.app[title].child_window(title=value).click_input()
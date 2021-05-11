# coding:utf-8


class ValueErr(Exception):
    """：value错误"""

    def __init__(self, message):
        self.message = message


class KeyErr(Exception):
    """：key错误"""

    def __init__(self, message):
        self.message = message


class TypeErr(Exception):
    """：type错误"""

    def __init__(self, message):
        self.message = message


class ProcessErr(Exception):
    """：进程错误"""
    def __init__(self, message="Calling process failed"):
        self.message = message


class InstallErr(Exception):
    """：安装错误"""
    def __init__(self, message="install Err"):
        self.message = message


class FileErr(Exception):
    """：文件错误"""
    def __init__(self, message):
        self.message = message

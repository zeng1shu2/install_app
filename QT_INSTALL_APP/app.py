# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


import multiprocessing
import os
import sys
from threading import Thread
from time import sleep
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from function import get_install
from function.install_class import Installer, check_config

fp = open('./Log/Setup_sys.log', 'a+')
stderr = sys.stderr
stdout = sys.stdout
sys.stderr = fp
sys.stdout = fp


class GuiApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.app_setup = Installer()
        self.process = multiprocessing
        self.setupUi()

    def setupUi(self):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.WindowModal)
        MainWindow.resize(268, 288)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("resource/install.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.tabWidget = QtWidgets.QTabWidget(MainWindow)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 271, 291))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.pushButton1 = QtWidgets.QPushButton(self.tab)
        self.pushButton1.setGeometry(QtCore.QRect(20, 110, 221, 41))
        self.pushButton1.setObjectName("pushButton1")
        self.pushButton3 = QtWidgets.QPushButton(self.tab)
        self.pushButton3.setGeometry(QtCore.QRect(20, 210, 221, 41))
        self.pushButton3.setObjectName("pushButton3")
        self.pushButton2 = QtWidgets.QPushButton(self.tab)
        self.pushButton2.setGeometry(QtCore.QRect(20, 160, 221, 41))
        self.pushButton2.setObjectName("pushButton2")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(90, 60, 151, 41))
        self.pushButton.setStyleSheet("\n""")
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 81, 16))
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(10, 10, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setObjectName("label")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.pushButton4 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton4.setGeometry(QtCore.QRect(20, 90, 221, 41))
        self.pushButton4.setObjectName("pushButton4")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.pushButton5 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton5.setGeometry(QtCore.QRect(20, 50, 221, 41))
        self.pushButton5.setObjectName("pushButton5")
        self.progressBar = QtWidgets.QProgressBar(self.tab_3)
        self.progressBar.setGeometry(QtCore.QRect(20, 110, 221, 31))
        self.progressBar.setToolTip("")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.tabWidget.addTab(self.tab_3, "")

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        # 创建计时器
        self.timer = QtCore.QBasicTimer()
        self.step = 0

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.pushButton5.setText('下载完成')
            return
        self.step = self.step + 1
        self.progressBar.setValue(self.step)
        if self.step == 30:
            check_config.check_path()
            get_install.vpn()
        if self.step == 60:
            get_install.agent()
        if self.step == 90:
            get_install.sdc()

        # 控制滚动条

    def running(self):
        if self.timer.isActive():
            self.timer.stop()
            self.pushButton5.setText('开始下载')
            self.progressBar.setMaximum(100)
        else:
            self.timer.start(100, self)
            self.pushButton5.setText('停止下载')
            self.progressBar.setMinimum(0)

    def install_all(self):
        """顺序安装"""
        q1 = multiprocessing.Queue()
        p1 = Thread(target=self.app_setup.vpn(), args=('p1', q1))
        p1.start()
        sleep(1)
        p2 = Thread(target=self.app_setup.agent(), args=('p2', q1))
        p2.start()
        sleep(1)
        p3 = Thread(target=self.app_setup.sdc(), args=('p3', q1))
        p3.start()

    def install_vpn(self):
        self.app_setup.vpn()

    def install_agent(self):
        self.app_setup.agent()

    def install_sdc(self):
        self.app_setup.sdc()

    def get_install1(self):
        pass

    @staticmethod
    def install_check():
        log = check_config
        log.check_vpn()
        log.check_agent()
        log.check_sdc()
        log.check_dns()

    def retranslateUi(self, _app):
        _translate = QtCore.QCoreApplication.translate
        _app.setWindowTitle(_translate("_app", "Environment"))
        self.pushButton1.setText(_translate("_app", "安装VPN客户端"))
        self.pushButton3.setText(_translate("_app", "安装沙盒客户端"))
        self.pushButton2.setText(_translate("_app", "安装准入客户端"))
        self.pushButton.setText(_translate("_app", "一键安装环境"))
        self.label_2.setText(_translate("_app", "全新环境：→"))
        self.label.setText(_translate("_app", "注意：安装过程中鼠标无法操作为正常现象。"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("_app", "环境安装"))
        self.pushButton4.setText(_translate("_app", "一键环境诊断"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("_app", "环境诊断"))
        self.pushButton5.setText(_translate("_app", "安装包下载"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("_app", "环境安装包下载"))
        # ######################################################################################
        # 一键安装检查
        check = check_config.check_dir()
        check = list(check)
        if self.pushButton.clicked.connect(self.msgg):
            if check[0] and check[1] and check[2]:
                self.pushButton.clicked.connect(self.msg)
            else:

                self.pushButton.clicked.connect(self.install_all)
        # ######################################################################################
        if self.pushButton1.clicked.connect(self.msgg):
            if os.path.exists("C:/Program Files (x86)/SecoClient/SecoClient.exe"):
                self.pushButton1.clicked.connect(self.msg2)
            else:
                self.pushButton1.clicked.connect(self.app_setup.vpn)
        if self.pushButton2.clicked.connect(self.msgg):
            if os.path.exists('c:/Windows/Agt3Tool.exe'):
                self.pushButton2.clicked.connect(self.msg2)
            else:
                self.pushButton2.clicked.connect(self.app_setup.agent)
        if self.pushButton3.clicked.connect(self.msgg):
            if os.path.exists('C:/Program Files/CnSinDa/SDC4/ClientL/x64/CliLSvc.exe'):
                self.pushButton3.clicked.connect(self.msg2)
            else:
                self.pushButton3.clicked.connect(self.app_setup.sdc)
        self.pushButton4.clicked.connect(self.install_check)
        self.pushButton4.clicked.connect(self.msg4)
        # 下载安装包 、绑定计时器
        if self.pushButton5.clicked.connect(self.msgg):
            result = check_config.check_setup()
            if result == 0:
                self.pushButton5.clicked.connect(self.msg3)
            else:
                self.pushButton5.clicked.connect(self.running)

    def msg4(self):
        # 使用infomation信息框
        QMessageBox.information(self.pushButton4, "提示", "收集完毕", QMessageBox.Yes)

    def msg3(self):
        QMessageBox.information(self.pushButton5, "提示",
                                "软件包已存在，请勿重复下载。如有疑问请将收集的日志发给管理员。", QMessageBox.Yes)

    def msg2(self):
        QMessageBox.information(self.pushButton1, "提示",
                                "此软件已安装，请不要重复安装，如有疑问请将收集的日志发给管理员。", QMessageBox.Yes)

    def msg(self):
        QMessageBox.information(self.pushButton, "提示",
                                "请查看是否已经安装过环境，如有疑问请将收集的日志发给管理员。", QMessageBox.Yes)

    def msgg(self):
        pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = GuiApp()
    MainWindow.show()
    sys.exit(app.exec_())
fp.close()
sys.stdout = stdout
sys.stderr = stderr

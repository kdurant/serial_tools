#-*- coding:utf-8 -*-
# -*- coding:utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import *

from extendFunction import *

class SerialUI(QMainWindow):
    def __init__(self):
        super(SerialUI, self).__init__()
        try:
            qss = open('serial.qss').read()
            self.setStyleSheet(qss)
        except:
            pass

        self.resize(800, 500)
        self.setWindowTitle('串口调试工具')
        self.setWindowIcon(QIcon('images/serialIcon.svg'))
        self.initUI()
        self.createToolBar()
        self.createStatusBar()

        self.helpWidget = QWidget()
        self.helpWidget.hide()

    def initUI(self):
        serialInfo = self.serialParaUI()
        recvSet = self.recvConfigUI()
        sendSet = self.sendConfigUI()
        recvData = self.recvdataUI()
        sendData = self.sendDataUI()
        self.extendUI = MutilString()
        self.extendUI.hide()

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(serialInfo)
        rightLayout.addWidget(recvSet)
        rightLayout.addWidget(sendSet)

        highLayout = QVBoxLayout()
        highLayout.addWidget(self.extendUI)

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(recvData)
        leftLayout.addWidget(sendData)

        mainLayout = QHBoxLayout()
        mainLayout.addLayout(rightLayout)
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(highLayout)

        mainLayout.setStretchFactor(rightLayout, 1)
        mainLayout.setStretchFactor(leftLayout, 3)
        mainLayout.setStretchFactor(highLayout, 1)
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def createToolBar(self):
        self.highAction = QAction(QIcon('images/high.svg'), "extend", self, triggered=self.showExtendUI)
        self.helpAction = QAction(QIcon('images/help.svg'), "help", self, triggered=self.showHelpWidget)
        toolbar = self.addToolBar('T')
        # new = QAction(QIcon("./images/new.png"), "new", self)
        toolbar.addAction(self.highAction)
        toolbar.addAction(self.helpAction)

    def createStatusBar(self):
        self.statusBar = QStatusBar()
        self.bar0 = QLabel()
        self.bar1 = QLabel()
        self.bar2 = QLabel()
        self.bar3 = QLabel()
        self.statusBar.addWidget(self.bar0, 1)
        self.statusBar.addWidget(self.bar1, 1)
        self.statusBar.addWidget(self.bar2, 1)
        self.statusBar.addWidget(self.bar3, 1)
        self.setStatusBar(self.statusBar)

    def serialParaUI(self):
        self.serialNumComb = QComboBox()
        self.serialBaudComb = QComboBox()
        self.serialBaudComb.addItems(['9600', '38400', '115200'])
        self.serialCheckComb = QComboBox()
        self.serialCheckComb.addItems(['None'])
        self.serialDataLenComb = QComboBox()
        self.serialDataLenComb.addItems(['8'])
        self.serialStopComb = QComboBox()
        self.serialStopComb.addItems(['1'])
        self.openBtn = QPushButton('打开串口')

        self.closeBtn = QPushButton('关闭串口')
        self.closeBtn.setEnabled(False)

        formLayout = QFormLayout()
        formLayout.addRow('串口号：', self.serialNumComb)
        formLayout.addRow('波特率：', self.serialBaudComb)
        formLayout.addRow('校验位：', self.serialCheckComb)
        formLayout.addRow('数据位：', self.serialDataLenComb)
        formLayout.addRow('停止位：', self.serialStopComb)
        formLayout.addRow(self.openBtn, self.closeBtn)

        groupBox = QGroupBox('串口设置')
        groupBox.setLayout(formLayout)

        return groupBox

    def recvConfigUI(self):
        self.writeDataToFileCb = QCheckBox('接受数据写入文件')
        self.autoWrapCb = QCheckBox('自动换行')
        self.autoWrapCb.setChecked(True)
        self.hexDisplayCb = QCheckBox('HEX显示')
        self.pauseReceiveCb = QCheckBox('暂停接受')
        self.saveRecvBtn = QPushButton('保存数据')
        self.saveRecvBtn.setToolTip('保存当前接受数据区的数据')
        self.clearRecvBtn = QPushButton('清除显示')

        vbox = QVBoxLayout()
        vbox.addWidget(self.writeDataToFileCb)
        vbox.addWidget(self.autoWrapCb)
        vbox.addWidget(self.hexDisplayCb)
        vbox.addWidget(self.pauseReceiveCb)
        vbox.addWidget(self.saveRecvBtn)
        vbox.addWidget(self.clearRecvBtn)

        groupBox = QGroupBox('接受设置')
        groupBox.setLayout(vbox)
        return groupBox

    def sendConfigUI(self):
        self.loadFileBtn = QPushButton('选择文件')
        self.hexSendCb = QCheckBox('HEX发送')
        self.timeSendCb = QCheckBox('定时发送ms：')
        self.sendBtn = QPushButton('发送')

        vbox = QVBoxLayout()
        vbox.addWidget(self.loadFileBtn)
        vbox.addWidget(self.hexSendCb)
        vbox.addWidget(self.timeSendCb)
        vbox.addWidget(self.sendBtn)

        groupBox = QGroupBox('发送设置')
        groupBox.setLayout(vbox)
        return groupBox

    def recvdataUI(self):
        self.recvText = QTextEdit()

        vbox = QVBoxLayout()
        vbox.addWidget(self.recvText)

        groupBox = QGroupBox('接收数据区')
        groupBox.setLayout(vbox)
        return groupBox

    def sendDataUI(self):
        self.sendEdit = QLineEdit()
        vbox = QVBoxLayout()
        vbox.addWidget(self.sendEdit)

        groupBox = QGroupBox('发送数据区')
        groupBox.setLayout(vbox)
        return groupBox

    def showExtendUI(self):
        if self.extendUI.isHidden():
            self.extendUI.show()
        else:
            self.extendUI.hide()

    def showHelpWidget(self):
        # self.helpWidget.show()
        if self.helpWidget.isHidden():
            self.helpWidget.show()
        else:
            self.helpWidget.hide()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = SerialUI()
    # ui = selectFile()
    ui.show()
    sys.exit(app.exec_())

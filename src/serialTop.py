# -*- coding:utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import *

class serialTop(QWidget):
    def __init__(self):
        super(serialTop, self).__init__()
        self.initUI()
        self.detectSerialStatus()

    def initUI(self):
        serialInfo = self.serialParaUI()
        receiveSet = self.receiveSetUI()

        rightLayout = QVBoxLayout()
        rightLayout.addWidget(serialInfo)
        rightLayout.addWidget(receiveSet)
        leftLayout = QVBoxLayout()


        mainLayout = QHBoxLayout()
        mainLayout.addLayout(rightLayout)
        mainLayout.addLayout(leftLayout)
        self.setLayout(mainLayout)

    def serialParaUI(self):
        self.serialNumComb = QComboBox()
        self.serialBaudComb = QComboBox()
        self.serialCheckComb = QComboBox()
        self.serialDataLenComb = QComboBox()
        self.serialStopComb = QComboBox()
        self.ctrlBtn = QPushButton('打开串口')

        formLayout = QFormLayout()
        formLayout.addRow('串口号：', self.serialNumComb)
        formLayout.addRow('波特率：', self.serialBaudComb)
        formLayout.addRow('校验位：', self.serialCheckComb)
        formLayout.addRow('数据位：', self.serialDataLenComb)
        formLayout.addRow('停止位：', self.serialStopComb)
        formLayout.addWidget(self.ctrlBtn)

        groupBox = QGroupBox('串口设置')
        groupBox.setLayout(formLayout)
        return groupBox

    def receiveSetUI(self):
        self.writeDataToFileCb = QCheckBox('接受数据写入文件')
        self.autoWrapCb = QCheckBox('自动换行')
        self.hexDisplayCb = QCheckBox('HEX显示')
        self.pauseReceiveCb = QCheckBox('暂停接受')
        self.saveBtn = QPushButton('保存数据')
        self.clearBtn = QPushButton('清除显示')

        vbox = QVBoxLayout()
        vbox.addWidget(self.writeDataToFileCb)
        vbox.addWidget(self.autoWrapCb)
        vbox.addWidget(self.hexDisplayCb)
        vbox.addWidget(self.pauseReceiveCb)
        vbox.addWidget(self.saveBtn)
        vbox.addWidget(self.clearBtn)

        groupBox = QGroupBox('接受设置')
        groupBox.setLayout(vbox)
        return groupBox

    def sendSetUI(self):
        self.loadFileBtn = QPushButton('发送文件')
        self.hexSendBtn = QCheckBox('HEX发送')

    def detectSerialStatus(self):
        available_ports = QSerialPortInfo.availablePorts()
        for port in available_ports:
            print(port)
            print(port.portName)
            # if not port.isBusy:
                # self.comboBox_SerialPort.addItem(port.portName()
                # print(port.portName)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = serialTop()
    # ui = selectFile()
    ui.show()
    sys.exit(app.exec_())

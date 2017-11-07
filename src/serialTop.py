# -*- coding:utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtSerialPort import *

from extendFunction import *

class serialTop(QMainWindow):
    def __init__(self):
        super(serialTop, self).__init__()
        self.com = QSerialPort()
        self.recvBytes = 0
        self.sendBytes = 0

        self.initUI()
        self.createToolBar()
        self.detectSerialStatus()
        self.signalSlot()
        self.setWindowTitle('串口调试工具')
        self.setWindowIcon(QIcon('images/serialIcon.svg'))

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

        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def createToolBar(self):
        self.new = QAction(QIcon('images/high.svg'), "extend", self, triggered=self.showExtendUI)
        toolbar = self.addToolBar('T')
        # new = QAction(QIcon("./images/new.png"), "new", self)
        toolbar.addAction(self.new)


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

    def sendConfigUI(self):
        self.loadFileBtn = QPushButton('发送文件')
        self.hexSendBtn = QCheckBox('HEX发送')
        self.timeSendCb = QCheckBox('定时发送ms：')

        vbox = QVBoxLayout()
        vbox.addWidget(self.loadFileBtn)
        vbox.addWidget(self.hexSendBtn)
        vbox.addWidget(self.timeSendCb)

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
        self.sendText = QLineEdit()
        vbox = QVBoxLayout()
        vbox.addWidget(self.sendText)

        groupBox = QGroupBox('发送数据区')
        groupBox.setLayout(vbox)
        return groupBox

    def detectSerialStatus(self):
        available_ports = QSerialPortInfo.availablePorts()
        for port in available_ports:
            # if not port.isBusy():
            self.serialNumComb.addItem(port.portName())

    def signalSlot(self):
        self.openBtn.clicked.connect(self.openCom)
        self.closeBtn.clicked.connect(self.closeCom)
        self.com.readyRead.connect(self.recvData)

    @pyqtSlot()
    def openCom(self):
        comName = self.serialNumComb.currentText()
        comBaud = int(self.serialBaudComb.currentText())
        self.com.setPortName(comName)
        try:
            if self.com.open(QSerialPort.ReadWrite) == False:
                QMessageBox.critecla(self, '打开失败', '该串口不存在或已被占用')
                return
            else:
                self.openBtn.setEnabled(False)
                self.closeBtn.setEnabled(True)
                return
        except:
            QMessageBox.critical(self, '打开失败', '该串口不存在或已被占用')
            return
        self.com.setBaudRate(comBaud)


    @pyqtSlot()
    def closeCom(self):
        if self.com.isOpen():
            self.com.close()
            self.openBtn.setEnabled(True)
            self.closeBtn.setEnabled(False)

    @pyqtSlot()
    def recvData(self):
        try:
            recvData = bytes(self.com.readAll())
        except:
            QMessageBox.critical(self, '错误', '串口接收错误')

    def showExtendUI(self):
        if self.extendUI.isHidden():
            self.extendUI.show()
            print(self.extendUI.isHidden())
        else:
            self.extendUI.hide()
        pass
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = serialTop()
    # ui = selectFile()
    ui.show()
    sys.exit(app.exec_())

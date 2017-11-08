# -*- coding:utf-8 -*-

# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtSerialPort import *

from serialUI import *
from extendFunction import *

class serialTop(SerialUI):
    def __init__(self):
        super(serialTop, self).__init__()
        self.com = QSerialPort()
        self.recvBytes = 0
        self.sendBytes = 0

        self.detectSerialStatus()
        self.signalSlot()

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

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
        self.recvCnt = 0
        self.sendCnt = 0

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
        self.clearRecvBtn.clicked.connect(self.clearRecvData)
        self.saveRecvBtn.clicked.connect(self.saveRecvData)

    @pyqtSlot()
    def openCom(self):
        comName = self.serialNumComb.currentText()
        comBaud = int(self.serialBaudComb.currentText())
        self.com.setPortName(comName)
        try:
            if self.com.open(QSerialPort.ReadWrite) == False:
                QMessageBox.critecla(self, '打开失败', '该串口不存在或已被占用')
                self.bar0.setText('串口状态: ' + '关闭')
                return
            else:
                self.openBtn.setEnabled(False)
                self.closeBtn.setEnabled(True)
                self.bar0.setText('串口状态: ' + '打开')

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
            self.bar0.setText('串口状态: ' + '关闭')

    @pyqtSlot()
    def recvData(self):
        try:
            recvData = bytes(self.com.readAll())
            self.recvCnt += len(recvData)
            if self.hexDisplayCb.isChecked():
                data = recvData
            else:
                data = recvData
        except:
            QMessageBox.critical(self, '错误', '串口接收错误')

        if not self.pauseReceiveCb.isChecked():
            if self.autoWrapCb.isChecked():
                self.recvText.append(data + '\n')
            else:
                self.recvText.append(data)

    @pyqtSlot()
    def sendData(self):
        data = self.sendEdit.text()
        if len(data) == 0:
            return
        if self.hexSendCb.isChecked():
            data = data
            n = self.com.write(data)
        else:
            n = self.com.write(data)
        self.sendCnt += n

    @pyqtSlot()
    def clearRecvData(self):
        self.recvText.clear()

    @pyqtSlot()
    def saveRecvData(self):
        filename = QFileDialog.getSaveFileName(self, 'save', 'serial.txt')
        try:
            with open(filename[0], 'w') as f:
                f.write(self.recvText.toPlainText())
        except:
            pass

    def showExtendUI(self):
        if self.extendUI.isHidden():
            self.extendUI.show()
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

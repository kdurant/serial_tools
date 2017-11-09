# -*- coding:utf-8 -*-
# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# from PyQt5.QtSerialPort import *
from binascii import a2b_hex, b2a_hex
from serialUI import *
from extendFunction import *

class serialTop(SerialUI):
    dataReady = pyqtSignal(bytes)
    def __init__(self):
        super(serialTop, self).__init__()
        self.com = QSerialPort()
        self.recvCnt = 0
        self.sendCnt = 0
        self.autoTimer = QTimer()

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
        self.timeSendCb.stateChanged.connect(self.startAutoTimer)
        self.sendBtn.clicked.connect(self.getData)
        self.dataReady[bytes].connect(self.sendData)
        self.autoTimer.timeout.connect(self.getData)

    @pyqtSlot()
    def openCom(self):
        comName = self.serialNumComb.currentText()
        self.com.setPortName(comName)
        try:
            if self.com.open(QSerialPort.ReadWrite) == False:
                QMessageBox.critecla(self, '打开失败', '该串口不存在或已被占用')
                self.serialStatusBar.setText('串口状态：Close')
                return
            else:
                self.openBtn.setEnabled(False)
                self.closeBtn.setEnabled(True)
                self.serialStatusBar.setText('串口状态：Open')
        except:
            QMessageBox.critical(self, '打开失败', '该串口不存在或已被占用')
            return
        self.com.setBaudRate(int(self.serialBaudComb.currentText()))
        self.com.setDataBits(int(self.serialDataLenComb.currentText()))
        self.com.setStopBits(int(self.serialStopComb.currentText()))

        self.serialNumComb.setEnabled(False)
        self.serialBaudComb.setEnabled(False)
        self.serialCheckComb.setEnabled(False)
        self.serialDataLenComb.setEnabled(False)
        self.serialStopComb.setEnabled(False)

    @pyqtSlot()
    def closeCom(self):
        if self.com.isOpen():
            self.com.close()
            self.openBtn.setEnabled(True)
            self.closeBtn.setEnabled(False)
            self.serialStatusBar.setText('串口状态：Close')

            self.serialNumComb.setEnabled(True)
            self.serialBaudComb.setEnabled(True)
            self.serialCheckComb.setEnabled(True)
            self.serialDataLenComb.setEnabled(True)
            self.serialStopComb.setEnabled(True)
            return

    @pyqtSlot()
    def recvData(self):
        '''
        当以非HEX方式发送数据时：
        发送 '12' : 收到的是 b'1', b'2'
        发送 '中文' : 收到的是 b'\xe4\xb8\xad', b'\xe6\x96\x87'
        可得出结论，发送数据为 s.encode('utf')
        接收到数据时，recv_s.decode('utf8')即可正确显示

        当以HEX方式发送数据时：
        发送 'ab' : 收到 b'\xab'
        :return:
        '''
        try:
            recvData = bytes(self.com.readAll())
            self.recvCnt += len(recvData)
            self.recvCntBar.setText('发送字节：' + str(self.recvCnt))

            if self.hexSendCb.isChecked():
                if self.hexDisplayCb.isChecked():
                    data = b2a_hex(recvData)
                    data = data.decode('utf8')
                else:
                    data = b2a_hex(recvData)
                    data = data.decode('utf8')
                    data = ''.join([str(ord(i)) for i in data])     # '34' -> '33 34'
            else:
                if self.hexDisplayCb.isChecked():
                    data = b2a_hex(recvData)
                    data = data.decode('utf8')
                else:
                    data = recvData.decode('utf8')
        except:
            QMessageBox.critical(self, '错误', '串口接收错误')

        if not self.pauseReceiveCb.isChecked():
            if self.autoWrapCb.isChecked():
                self.recvText.insertPlainText(data + '\n')
            else:
                self.recvText.insertPlainText(data)

    @pyqtSlot()
    def getData(self):
        '''
        从发送文本框里获得需要发送的字符串
        :return:
        '''
        if self.openBtn.isEnabled():
            QMessageBox.warning(self, '警告', '请先打开串口')
            return

        data = self.sendEdit.text()
        if len(data) == 0:
            QMessageBox.warning(self, '警告', '不能发送空内容')
            return
        if self.hexSendCb.isChecked():
            data = data.replace(' ', '')
            if len(data) % 2 == 0:
                data = a2b_hex(data)
                self.dataReady.emit(data)
            else:
                QMessageBox.warning(self, '警告', '十六进制数不是偶数个')
                return
        else:
            data = data.encode('utf8')
            self.dataReady.emit(data)

    @pyqtSlot(bytes)
    def sendData(self, data):
        '''
        ascii 方式发送 '34', HEX显示为 '33 34'; ascii显示为 '34'
        hex 方式发送 '34', HEX显示为 '34'; ascii显示为 '4'
        :return:
        '''
        n = self.com.write(data)
        self.sendCnt += n
        self.sendCntBar.setText('发送字节：' + str(self.sendCnt))

    @pyqtSlot()
    def clearRecvData(self):
        self.recvText.clear()
        self.recvCnt = 0
        self.sendCnt = 0
        self.sendCntBar.setText('发送字节：0')
        self.recvCntBar.setText('发送字节：0')

    @pyqtSlot()
    def saveRecvData(self):
        if self.recvText.toPlainText():
            filename = QFileDialog.getSaveFileName(self, 'save', 'serial.txt')
            try:
                with open(filename[0], 'w') as f:
                    f.write(self.recvText.toPlainText())
            except:
                pass
        else:
            QMessageBox.warning(self, '警告', '不能保存空白内容')

    @pyqtSlot()
    def startAutoTimer(self):
        if self.timeSendCb.isChecked():
            self.autoTimer.start(int(self.timeEdit.text()))
        else:
            self.autoTimer.stop()

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

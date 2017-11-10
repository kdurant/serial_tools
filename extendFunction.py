#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MutilString(QWidget):
    '''
    可设置发送多条字符串
    '''
    dataReady = pyqtSignal(str)
    def __init__(self):
        super(MutilString, self).__init__()
        self.selCbList = []
        self.hexEditList = []
        self.sendBtnList = []

        self.timer = QTimer()
        self.initUI()
        self.signalSlot()

    def initUI(self):
        t = self.haha()
        vbox = QHBoxLayout()
        vbox.addWidget(t)
        self.setLayout(vbox)

    def haha(self):
        grid = QGridLayout()
        for i in range(0, 8):
            self.selCbList.append(QCheckBox())
            self.hexEditList.append(QLineEdit())
            btn = QPushButton(str(i))
            btn.setFixedWidth(30)
            self.sendBtnList.append(btn)
            self.sendBtnList[i].clicked.connect(self.sendSingleStr)
            row = i + 1
            grid.addWidget(self.selCbList[i], row, 0)
            grid.addWidget(self.hexEditList[i], row, 1)
            grid.addWidget(self.sendBtnList[i], row, 2)

        selLabel = QLabel('选择')
        strLabel = QLabel('字符串')
        sendLabel = QLabel('发送')

        grid.addWidget(selLabel, 0, 0)
        grid.addWidget(strLabel, 0, 1)
        grid.addWidget(sendLabel, 0, 2)


        self.cycleSendCb = QCheckBox('循环发送')
        self.hexSendCb = QCheckBox('hex发送')
        self.hexSendCb.setChecked(True)

        hbox = QHBoxLayout()
        hbox.addWidget(self.cycleSendCb)
        hbox.addWidget(self.hexSendCb)

        self.cycleInterTimeEdit = QLineEdit('1000')
        self.strInterTimeEdit = QLineEdit('50')
        form = QFormLayout()
        form.addRow('大循环间隔时间(ms)：', self.cycleInterTimeEdit)
        form.addRow('字符串间隔时间(ms)：', self.strInterTimeEdit)

        vbox = QVBoxLayout()
        vbox.addLayout(grid)
        vbox.addLayout(hbox)
        vbox.addLayout(form)
        vbox.addStretch()

        # self.setLayout(vbox)

        frame = QFrame()
        frame.setLayout(vbox)

        s = QScrollArea()
        s.setWidget(frame)
        s.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        s.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        s.setWidgetResizable(True)
        return s

    def signalSlot(self):
        self.cycleSendCb.stateChanged.connect(self. startCycleTime)
        self.timer.timeout.connect(self.prepareData)
        pass
    @pyqtSlot()
    def startCycleTime(self):
        if self.cycleSendCb.isChecked():
            self.timer.start(int(self.cycleInterTimeEdit.text()))
        else:
            self.timer.stop()

    @pyqtSlot()
    def prepareData(self):
        for i in range(0, 8):
            if self.selCbList[i].isChecked():
                data = self.hexEditList[i].text()
                print(data)
                self.dataReady.emit(data)
                QThread.msleep(int(self.timeEdit.text()))
        pass

    def sendSingleStr(self):
        sender = self.sender()
        num = int(sender.text())
        data = self.hexEditList[num].text()
        if data:
            print(data)
        else:
            QMessageBox.warning(self, '警告', '发送内容不能为空')

class ProtocalFrame(QWidget):
    def __init__(self):
        super(ProtocalFrame, self).__init__()
        pass

class ExtendFunction(QWidget):
    def __init__(self):
        super(ExtendFunction, self).__init__()

        mutilString = MutilString()

        vbox = QVBoxLayout()
        vbox.addWidget(mutilString)

        self.setLayout(vbox)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    ui = ExtendFunction()
    # ui = selectFile()
    ui.show()
    sys.exit(app.exec_())

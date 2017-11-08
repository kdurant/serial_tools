#-*- coding:utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class MutilString(QWidget):
    '''
    可设置发送多条字符串
    '''
    def __init__(self):
        super(MutilString, self).__init__()

        hexCb0 = QCheckBox()
        hexCb1 = QCheckBox()
        hexCb2 = QCheckBox()
        hexCb3 = QCheckBox()
        hexCb4 = QCheckBox()
        hexCb5 = QCheckBox()
        hexCb6 = QCheckBox()
        hexCb7 = QCheckBox()

        hexEdit0 = QLineEdit()
        hexEdit1 = QLineEdit()
        hexEdit2 = QLineEdit()
        hexEdit3 = QLineEdit()
        hexEdit4 = QLineEdit()
        hexEdit5 = QLineEdit()
        hexEdit6 = QLineEdit()
        hexEdit7 = QLineEdit()

        sendBtn0 = QPushButton('0')
        sendBtn1 = QPushButton('1')
        sendBtn2 = QPushButton('2')
        sendBtn3 = QPushButton('3')
        sendBtn4 = QPushButton('4')
        sendBtn5 = QPushButton('5')
        sendBtn6 = QPushButton('6')
        sendBtn7 = QPushButton('7')

        hexLabel = QLabel('Hex')
        strLabel = QLabel('字符串')
        sendLabel = QLabel('发送')

        autoSendCb = QCheckBox('循环发送')
        intervalLabel = QLabel('间隔：ms')
        timeEdit = QLineEdit('1000')

        grid = QGridLayout()
        grid.addWidget(hexLabel, 0, 0)
        grid.addWidget(strLabel, 0, 1)
        grid.addWidget(sendLabel, 0, 2)
        grid.addWidget(hexCb0, 1, 0)
        grid.addWidget(hexCb1, 2, 0)
        grid.addWidget(hexCb2, 3, 0)
        grid.addWidget(hexCb3, 4, 0)
        grid.addWidget(hexCb4, 5, 0)
        grid.addWidget(hexCb5, 6, 0)
        grid.addWidget(hexCb6, 7, 0)
        grid.addWidget(hexCb7, 8, 0)

        grid.addWidget(hexEdit0, 1, 1)
        grid.addWidget(hexEdit1, 2, 1)
        grid.addWidget(hexEdit2, 3, 1)
        grid.addWidget(hexEdit3, 4, 1)
        grid.addWidget(hexEdit4, 5, 1)
        grid.addWidget(hexEdit5, 6, 1)
        grid.addWidget(hexEdit6, 7, 1)
        grid.addWidget(hexEdit7, 8, 1)

        grid.addWidget(sendBtn0, 1, 2)
        grid.addWidget(sendBtn1, 2, 2)
        grid.addWidget(sendBtn2, 3, 2)
        grid.addWidget(sendBtn3, 4, 2)
        grid.addWidget(sendBtn4, 5, 2)
        grid.addWidget(sendBtn5, 6, 2)
        grid.addWidget(sendBtn6, 7, 2)
        grid.addWidget(sendBtn7, 8, 2)

        grid.addWidget(intervalLabel, 10, 1)
        grid.addWidget(timeEdit, 10, 2)
        grid.addWidget(autoSendCb, 11, 1)

        self.setLayout(grid)

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

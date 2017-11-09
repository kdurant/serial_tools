#-*- coding:utf-8 -*-
# -*- coding:utf-8 -*-

__version__ = 'v0.0.2'
__autor__ = 'kdurant'

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
        self.hexSendRbtn.clicked.connect(self.editValidator)
        self.asciiSendRbtn.clicked.connect(self.editValidator)

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

        mainLayout.setStretchFactor(leftLayout, 3)
        mainLayout.setStretchFactor(highLayout, 1)
        widget = QWidget()
        widget.setLayout(mainLayout)
        self.setCentralWidget(widget)

    def createToolBar(self):
        self.highAction = QAction(QIcon('images/high.svg'), "extend", self, triggered=self.showExtendUI)
        self.helpAction = QAction(QIcon('images/help.svg'), "help", self, triggered=self.showHelpWidget)
        self.aboutAction = QAction(QIcon('images/aboutTool.svg'), "about", self, triggered=self.aboutTool)
        toolbar = self.addToolBar('T')
        # new = QAction(QIcon("./images/new.png"), "new", self)
        toolbar.addAction(self.highAction)
        toolbar.addAction(self.aboutAction)
        toolbar.addAction(self.helpAction)

    def createStatusBar(self):
        self.statusBar = QStatusBar()
        self.serialStatusBar = QLabel('串口状态：Close')
        self.recvCntBar = QLabel('接收字节：0')
        self.sendCntBar = QLabel('发送字节：0')
        self.bar3 = QLabel()
        self.statusBar.addWidget(self.serialStatusBar, 1)
        self.statusBar.addWidget(self.recvCntBar, 1)
        self.statusBar.addWidget(self.sendCntBar, 1)
        self.statusBar.addWidget(self.bar3, 1)
        self.setStatusBar(self.statusBar)

    def serialParaUI(self):
        self.serialNumComb = QComboBox()
        self.serialBaudComb = QComboBox()
        self.serialBaudComb.addItems(['9600', '14400', '38400', '56000', '57600', '115200', '128000'])
        self.serialCheckComb = QComboBox()
        self.serialCheckComb.addItems(['None'])
        self.serialDataLenComb = QComboBox()
        self.serialDataLenComb.addItems(['5', '6', '7', '8'])
        self.serialDataLenComb.setCurrentText('8')
        self.serialStopComb = QComboBox()
        self.serialStopComb.addItems(['1', '2'])
        self.openBtn = QPushButton('打开串口')
        self.openBtn.setObjectName('openBtn')

        self.closeBtn = QPushButton('关闭串口')
        self.closeBtn.setEnabled(False)

        formLayout = QFormLayout()
        formLayout.addRow('串口号：', self.serialNumComb)
        formLayout.addRow('波特率：', self.serialBaudComb)
        formLayout.addRow('校验位：', self.serialCheckComb)
        formLayout.addRow('数据位：', self.serialDataLenComb)
        formLayout.addRow('停止位：', self.serialStopComb)

        hbox = QHBoxLayout()
        hbox.addWidget(self.openBtn)
        hbox.addWidget(self.closeBtn)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(formLayout)
        mainLayout.addLayout(hbox)

        groupBox = QGroupBox('串口设置')
        groupBox.setLayout(mainLayout)

        return groupBox

    def recvConfigUI(self):
        self.hexSendRbtn = QRadioButton('HEX')
        self.asciiSendRbtn = QRadioButton('ASCII')
        self.hexSendRbtn.setChecked(True)

        self.writeDataToFileCb = QCheckBox('接受数据写入文件')
        self.autoWrapCb = QCheckBox('自动换行')
        self.autoWrapCb.setChecked(True)
        self.pauseReceiveCb = QCheckBox('暂停接收')
        self.saveRecvBtn = QPushButton('保存数据')
        self.saveRecvBtn.setToolTip('保存当前接受数据区的数据')
        self.clearRecvBtn = QPushButton('清除显示')

        hbox = QHBoxLayout()
        hbox.addWidget(self.asciiSendRbtn)
        hbox.addWidget(self.hexSendRbtn)

        vbox = QVBoxLayout()
        vbox.addWidget(self.writeDataToFileCb)
        vbox.addWidget(self.autoWrapCb)
        vbox.addWidget(self.pauseReceiveCb)
        vbox.addWidget(self.saveRecvBtn)
        vbox.addWidget(self.clearRecvBtn)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(hbox)
        mainLayout.addLayout(vbox)

        groupBox = QGroupBox('接受设置')
        groupBox.setLayout(mainLayout)
        return groupBox

    def sendConfigUI(self):
        self.hexSendRbtn = QRadioButton('HEX')
        self.asciiSendRbtn = QRadioButton('ASCII')
        self.hexSendRbtn.setChecked(True)

        self.timeSendCb = QCheckBox('定时发送(ms)：')
        self.timeEdit = QLineEdit('1000')

        hbox = QHBoxLayout()
        hbox.addWidget(self.asciiSendRbtn)
        hbox.addWidget(self.hexSendRbtn)

        vbox = QVBoxLayout()
        vbox.addWidget(self.timeSendCb)
        vbox.addWidget(self.timeEdit)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(hbox)
        mainLayout.addLayout(vbox)
        groupBox = QGroupBox('发送设置')
        groupBox.setLayout(mainLayout)
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
        self.sendEdit.setToolTip('HEX模式时，发送的数据不包括空格')
        self.sendEdit.setValidator(QRegExpValidator(QRegExp("[a-fA-F0-9 ]+$")))
        self.loadFileBtn = QPushButton('选择文件')
        self.loadFileEdit = QLineEdit()
        self.loadFileEdit.setReadOnly(True)
        self.sendBtn = QPushButton('发送')
        self.sendFileBtn = QPushButton('发送文件')
        self.sendFileBtn.setToolTip('文件只支持以ASCII码发送')

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.loadFileBtn)
        hbox1.addWidget(self.loadFileEdit)
        hbox1.addWidget(self.sendFileBtn)

        vbox = QHBoxLayout()
        vbox.addWidget(self.sendEdit)
        vbox.addWidget(self.sendBtn)

        mainLayout = QVBoxLayout()
        mainLayout.addLayout(vbox)
        mainLayout.addLayout(hbox1)

        groupBox = QGroupBox('发送数据区')
        groupBox.setLayout(mainLayout)
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

    @pyqtSlot()
    def editValidator(self):
        if self.hexSendRbtn.isChecked():
            self.sendEdit.setValidator(QRegExpValidator(QRegExp("[a-fA-F0-9 ]+$")))
        else:
            self.sendEdit.setValidator(QRegExpValidator(QRegExp(".*")))

    @pyqtSlot()
    def aboutTool(self):
        QMessageBox.about(self, "介绍", "verison：" + __version__ + "\n" 
                                        "autor：" + __autor__ + "\n"
                                        'github: https://github.com/durant'
                                        )

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ui = SerialUI()
    # ui = selectFile()
    ui.show()
    sys.exit(app.exec_())

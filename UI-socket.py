import os
import sys
import threading
import pyaudio
from PyQt5 import QtCore, QtWebSockets, QtNetwork, QtGui, QtWidgets
import time
import faulthandler
faulthandler.enable()

from scripts import task1_run, task2_run, task8_run, task9_run

sys.path.append("..")
from utils import VoiceRecorder, VoicePlayer



class MyServer():
    def __init__(self, name, ui):
        self.ui = ui
        self.server = QtWebSockets.QWebSocketServer(name, QtWebSockets.QWebSocketServer.NonSecureMode)
        self.server.acceptError.connect(self.onAcceptError)
        self.server.newConnection.connect(self.onNewConnection)
        self.port = 1302
        self.clients = []

    def setup(self):
        if self.server.listen(QtNetwork.QHostAddress.Any, self.port):
            print(f"INFO: Listening {self.server.serverName()}:{self.server.serverAddress().toString()}:{str(self.server.serverPort())}")
            for address in QtNetwork.QNetworkInterface().allAddresses():
                if address.protocol() == QtNetwork.QAbstractSocket.IPv4Protocol and address.toString() != "127.0.0.1":
                    print(address.toString())
                    self.ui.label_ipaddr.setText(f"{address.toString()}:{self.port}")
            # print(QtNetwork.QNetworkInterface().allAddresses()[1].toString())
        else:
            print("WARNING: server already listening")
            return
        self.clientConnection = None
        print("INFO: server set up", self.server.isListening())
        self.ui.label_connect.setText("Listening..")
        self.ui.button_setupserver.setEnabled(False)
        self.ui.button_closeserver.setEnabled(True)

    def close(self):
        for client in self.clients:  
            client.close()
        self.server.close()
        print("INFO: server closed", self.server.isListening())
        self.ui.label_connect.setText("Closed")
        self.ui.button_setupserver.setEnabled(True)
        self.ui.button_closeserver.setEnabled(False)


    def send_message(self, message):
        if len(self.clients) > 0:
            for client in self.clients:  
                client.sendTextMessage(message)
            return True
        return False

    def send_binary(self, binary):
        if len(self.clients) > 0:
            for client in self.clients:  
                client.sendBinaryMessage(binary)
            return True
        return False

    def receive_message(self, message):
        self.ui.receive_message(message)
    
    def receive_binary(self, message):
        self.ui.receive_binary(message)


    def onAcceptError(accept_error):
        print("INFO: Accept Error: {}".format(accept_error))

    def onNewConnection(self):
        print("INFO: new Client connected!")
        self.clientConnection = self.server.nextPendingConnection()

        self.clientConnection.textMessageReceived.connect(self.receive_message)
        self.clientConnection.disconnected.connect(self.socketDisconnected)
        self.clientConnection.binaryMessageReceived.connect(self.receive_binary)
        self.clients.append(self.clientConnection)
        self.ui.label_connect.setText("Connected")
        self.ui.init_message()

    def socketDisconnected(self):
        print("INFO: socket disconnected")
        if self.clientConnection:
            self.clients.remove(self.clientConnection)
            self.clientConnection.deleteLater()
        if self.server.isListening():
            self.ui.label_connect.setText("Listening..")
    
    def is_connected(self):
        return len(self.clients) > 0




class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Server")
        desktop_size = QtWidgets.QDesktopWidget().availableGeometry(self)
        self.resize(int(desktop_size.width()*0.3), int(desktop_size.height()*0.5))
        # uic.loadUi("mainwindow.ui", self)
        self.server = MyServer("Server", self)
        self.show()
        self.build()
        self.server.setup()
        self.recorder = None       
        self.log_file = None          

    def build(self):
        # central widget: widget
        widget = QtWidgets.QWidget()
        self.setCentralWidget(widget)
        layout = QtWidgets.QVBoxLayout()
        widget.setLayout(layout)

        # add layout
        layout_server = QtWidgets.QHBoxLayout()
        self.label_ipaddr = QtWidgets.QLabel("ip addr")
        self.button_setupserver = QtWidgets.QPushButton("Setup Server")
        self.button_setupserver.clicked.connect(self.server.setup)
        self.button_closeserver = QtWidgets.QPushButton("Close Server")
        self.button_closeserver.clicked.connect(self.server.close)
        layout_server.addWidget(self.label_ipaddr)
        layout_server.addWidget(self.button_setupserver)
        layout_server.addWidget(self.button_closeserver)
        layout.addLayout(layout_server)

        layout_info = QtWidgets.QHBoxLayout()
        self.label_connect = QtWidgets.QLabel("status")
        self.label_ipaddr.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        button_clear = QtWidgets.QPushButton("Clear Text")
        layout_info.addWidget(self.label_connect)
        layout_info.addWidget(button_clear)
        layout.addLayout(layout_info)

        self.text_edit = QtWidgets.QTextEdit()
        self.text_edit.setReadOnly(True)
        button_clear.clicked.connect(self.text_edit.clear)
        layout.addWidget(self.text_edit)

        layout_line = QtWidgets.QHBoxLayout()
        self.line_edit = QtWidgets.QLineEdit()
        self.line_edit.setClearButtonEnabled(True)
        button_send = QtWidgets.QPushButton("Send")
        button_send.clicked.connect(lambda: self.send_message("button"))
        self.button_send_voice = QtWidgets.QPushButton("")
        self.button_send_voice.setIcon(QtGui.QIcon("../image/voice1.png"))
        self.button_send_voice.clicked.connect(self.send_voice)
        layout_line.addWidget(self.line_edit)
        layout_line.addWidget(button_send)
        layout_line.addWidget(self.button_send_voice)
        layout.addLayout(layout_line)
        self.line_edit.returnPressed.connect(button_send.click)

        layout_console = QtWidgets.QVBoxLayout()
        label_console = QtWidgets.QLabel("Console")

        layout_task1 = QtWidgets.QHBoxLayout()
        button_task1 = QtWidgets.QPushButton("任务1")
        button_task1.clicked.connect(lambda: self.send_message("task1"))
        button_task1_run = QtWidgets.QPushButton("任务1_run")
        button_task1_run.clicked.connect(lambda: task1_run(self.server))
        layout_task1.addWidget(button_task1)
        layout_task1.addWidget(button_task1_run)

        layout_task2 = QtWidgets.QHBoxLayout()
        button_task2 = QtWidgets.QPushButton("任务2")
        button_task2.clicked.connect(lambda: self.send_message("task2"))
        button_task2_run = QtWidgets.QPushButton("任务2_run")
        button_task2_run.clicked.connect(lambda: task2_run(self.server))
        layout_task2.addWidget(button_task2)
        layout_task2.addWidget(button_task2_run)

        layout_task3 = QtWidgets.QHBoxLayout()
        button_task3 = QtWidgets.QPushButton("任务3")
        button_task3.clicked.connect(lambda: self.send_message("task3"))
        # button_task3_run = QtWidgets.QPushButton("任务3_run")
        # button_task3_run.clicked.connect(lambda: task3_run(self.server))
        layout_task3.addWidget(button_task3)
        # layout_task3.addWidget(button_task3_run)

        layout_task4 = QtWidgets.QHBoxLayout()
        button_task4 = QtWidgets.QPushButton("任务4")
        button_task4.clicked.connect(lambda: self.send_message("task4"))
        button_task4_run = QtWidgets.QPushButton("任务4_run")
        button_task4_run.clicked.connect(lambda: self.send_message("task4_run"))
        layout_task4.addWidget(button_task4)
        layout_task4.addWidget(button_task4_run)

        layout_task5 = QtWidgets.QHBoxLayout()
        button_task5 = QtWidgets.QPushButton("任务5")
        button_task5.clicked.connect(lambda: self.send_message("task5"))
        # button_task5_run = QtWidgets.QPushButton("任务4_run")
        # button_task5_run.clicked.connect(lambda: self.send_message("task4_run"))
        layout_task5.addWidget(button_task5)
        # layout_task5.addWidget(button_task5_run)

        layout_task6 = QtWidgets.QHBoxLayout()
        button_task6 = QtWidgets.QPushButton("任务6")
        button_task6.clicked.connect(lambda: self.send_message("task6"))
        # button_task5_run = QtWidgets.QPushButton("任务4_run")
        # button_task5_run.clicked.connect(lambda: self.send_message("task4_run"))
        layout_task6.addWidget(button_task6)
        # layout_task5.addWidget(button_task5_run)

        layout_task7 = QtWidgets.QHBoxLayout()
        button_task7 = QtWidgets.QPushButton("任务7")
        button_task7.clicked.connect(lambda: self.send_message("task7"))
        # button_task5_run = QtWidgets.QPushButton("任务4_run")
        # button_task5_run.clicked.connect(lambda: self.send_message("task4_run"))
        layout_task7.addWidget(button_task7)
        # layout_task5.addWidget(button_task5_run)

        layout_task8 = QtWidgets.QHBoxLayout()
        button_task8 = QtWidgets.QPushButton("任务8")
        button_task8.clicked.connect(lambda: self.send_message("task8"))
        button_task8_run = QtWidgets.QPushButton("任务8_run")
        button_task8_run.clicked.connect(lambda: task8_run(self.server))
        layout_task8.addWidget(button_task8)
        layout_task8.addWidget(button_task8_run)

        layout_task9 = QtWidgets.QHBoxLayout()
        button_task9 = QtWidgets.QPushButton("任务9")
        button_task9.clicked.connect(lambda: self.send_message("task9"))
        # button_task9_run = QtWidgets.QPushButton("任务9_run")
        # button_task9_run.clicked.connect(lambda: task9_run(self.server))
        layout_task9.addWidget(button_task9)
        # layout_task9.addWidget(button_task9_run)
        
        # layout_tasks = QtWidgets.QHBoxLayout()
        # button_1 = QtWidgets.QPushButton("1")
        # button_1.clicked.connect(lambda: self.send_message("1"))
        # layout_tasks.addWidget(button_1)
        # button_2 = QtWidgets.QPushButton("2")
        # button_2.clicked.connect(lambda: self.send_message("2"))
        # layout_tasks.addWidget(button_2)
        # button_3 = QtWidgets.QPushButton("3")
        # button_3.clicked.connect(lambda: self.send_message("3"))
        # layout_tasks.addWidget(button_3)
        # button_4 = QtWidgets.QPushButton("4")
        # button_4.clicked.connect(lambda: self.send_message("4"))
        # layout_tasks.addWidget(button_4)
        # button_5 = QtWidgets.QPushButton("5")
        # button_5.clicked.connect(lambda: self.send_message("5"))
        # layout_tasks.addWidget(button_5)
        # button_6 = QtWidgets.QPushButton("6")
        # button_6.clicked.connect(lambda: self.send_message("6"))
        # layout_tasks.addWidget(button_6)
        # button_7 = QtWidgets.QPushButton("7")
        # button_7.clicked.connect(lambda: self.send_message("7"))
        # layout_tasks.addWidget(button_7)
        # button_8 = QtWidgets.QPushButton("8")
        # button_8.clicked.connect(lambda: self.send_message("8"))
        # layout_tasks.addWidget(button_8)
        # button_9 = QtWidgets.QPushButton("9")
        # button_9.clicked.connect(lambda: self.send_message("9"))
        # layout_tasks.addWidget(button_9)

        layout_console.addWidget(label_console)
        layout_console.addLayout(layout_task1)
        layout_console.addLayout(layout_task2)
        layout_console.addLayout(layout_task3)
        layout_console.addLayout(layout_task4)
        layout_console.addLayout(layout_task5)
        layout_console.addLayout(layout_task6)
        layout_console.addLayout(layout_task7)
        layout_console.addLayout(layout_task8)
        layout_console.addLayout(layout_task9)

        # layout_console.addLayout(layout_tasks)

        layout.addLayout(layout_console)

    def init_message(self):
        prefix = os.path.join(os.path.dirname(__file__), '../log')
        if not os.path.exists(prefix):
            os.mkdir(prefix)
        log_name = "log_" + time.strftime('%m%d%H%M%S', time.localtime(time.time()))
        filename = log_name+'.txt'
        self.log_file = open(os.path.join(prefix, filename), "a", encoding="UTF-8")
        self.voice_dir_path= os.path.join(prefix, log_name)
        os.mkdir(self.voice_dir_path)

    def save_message_server(self,message):
        self.log_file.write('wizard: ')
        self.log_file.write(message)
        self.log_file.write('\n')

    def save_message_client(self,message):
        self.log_file.write('user: ')
        self.log_file.write(message)
        self.log_file.write('\n')

    def save_voice_server(self,binary):
        voice_name= "voice_"+time.strftime('%m%d%H%M%S', time.localtime(time.time()))
        self.log_file.write('wizard: ')
        self.log_file.write(voice_name)
        self.log_file.write('\n')
        player = VoicePlayer(binary)
        player.save(self.voice_dir_path+"/"+voice_name+"_wizard.wav")

    def save_voice_client(self,binary):
        voice_name= "voice_"+time.strftime('%m%d%H%M%S', time.localtime(time.time()))
        self.log_file.write('user: ')
        self.log_file.write(voice_name)
        self.log_file.write('\n')
        player = VoicePlayer(binary)
        player.save(self.voice_dir_path + "/" + voice_name + "_user.wav")

    def send_message(self, message):
        if message == "button":
            message = self.line_edit.text()
        if message == "" or message == False:
            return
        if self.server.send_message(message):
            if not message.startswith("task"):
                self.text_edit.append(f"{message}")
                cursor = self.text_edit.textCursor()
                textBlockFormat = cursor.blockFormat()
                textBlockFormat.setAlignment(QtCore.Qt.AlignRight)
                textBlockFormat.setLeftMargin(int(self.width()*0.3))
                textBlockFormat.setRightMargin(0)
                textBlockFormat.setTopMargin(3)
                textBlockFormat.setBottomMargin(3)
                # textBlockFormat.setBackground(QtCore.Qt.cyan)
                cursor.mergeBlockFormat(textBlockFormat)
                self.text_edit.setTextCursor(cursor)

                self.line_edit.clear()

            self.save_message_server(message)


    def send_voice(self):
        if not self.server.is_connected():
            return
        if self.recorder:
            self.recorder.stop_record()
            bdata = QtCore.QByteArray(self.recorder.get_frame())
            head = QtCore.QByteArray(1,'v')
            bdata = head + bdata
            self.server.send_binary(bdata)
            del(self.recorder)
            self.recorder = None
            self.button_send_voice.setIcon(QtGui.QIcon("../image/voice1.png"))

            message = "（语音消息）"
            self.text_edit.append(f"{message}")
            cursor = self.text_edit.textCursor()
            textBlockFormat = cursor.blockFormat()
            textBlockFormat.setAlignment(QtCore.Qt.AlignRight)
            textBlockFormat.setRightMargin(0)
            textBlockFormat.setTopMargin(3)
            textBlockFormat.setBottomMargin(3)
            cursor.mergeBlockFormat(textBlockFormat)
            self.text_edit.setTextCursor(cursor)
            self.save_voice_server(bdata)
        else:
            self.recorder = VoiceRecorder()
            self.recorder.start_record()
            self.button_send_voice.setIcon(QtGui.QIcon("../image/voice2.png"))

    def receive_message(self, message):
        self.text_edit.append(f"{message}")
        cursor = self.text_edit.textCursor()
        textBlockFormat = cursor.blockFormat()
        textBlockFormat.setAlignment(QtCore.Qt.AlignLeft)
        textBlockFormat.setRightMargin(int(self.width()*0.3))
        textBlockFormat.setLeftMargin(0)
        textBlockFormat.setTopMargin(3)
        textBlockFormat.setBottomMargin(3)
        cursor.mergeBlockFormat(textBlockFormat)
        self.text_edit.setTextCursor(cursor)
        self.save_message_client(message)

    def receive_binary(self, binary):
        message = "（语音消息）"
        self.text_edit.append(f"{message}")
        cursor = self.text_edit.textCursor()
        textBlockFormat = cursor.blockFormat()
        textBlockFormat.setAlignment(QtCore.Qt.AlignLeft)
        textBlockFormat.setLeftMargin(0)
        textBlockFormat.setTopMargin(3)
        textBlockFormat.setBottomMargin(3)
        cursor.mergeBlockFormat(textBlockFormat)
        self.text_edit.setTextCursor(cursor)
        self.save_voice_client(binary)

        if QtWidgets.QMessageBox.question(self, u'新语音消息', u"您有一条来自智能助手的语音消息。是否播放？", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes) == QtWidgets.QMessageBox.Yes:
            player = VoicePlayer(binary)
            player.start()

            

    def closeEvent(self, event):
        self.log_file.close()
        self.server.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    window = MainWindow()
    app.exec_()

    print("Closing from UI")
    quit()

import sys
import csv
import can, struct
from can.interfaces.vector.canlib import *
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QThread, Qt
from time import sleep
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QTabWidget, QPlainTextEdit, QProgressBar, QScrollBar, QSlider
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout

class Diagnostyk(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.addTab(self.tab1, "CAN CONFIG")
        self.addTab(self.tab2, "HCP1 CONTROL")

        self.interfejs()

    def interfejs(self):
        label_interfacetype = QLabel("CAN Interface Type", self)
        label_interfacechannel = QLabel("CAN Interface Channel", self)
        label_interfacespeed = QLabel("CAN Interface Speed", self)
        label_fd_interfacespeed = QLabel("FD data Speed", self)


        self.text_interfacetype = QPlainTextEdit()
        self.combo_interfacetype = QComboBox(self)
        self.combo_interfacetype.addItem("CAN HS")
        self.combo_interfacetype.addItem("CAN FD")

        self.combo_interfacechannel = QComboBox(self)
        self.combo_interfacechannel.addItem("1")
        self.combo_interfacechannel.addItem("2")

        self.combo_interfacespeed = QComboBox(self)
        self.combo_interfacespeed.addItem("100000")
        self.combo_interfacespeed.addItem("250000")
        self.combo_interfacespeed.addItem("500000")
        self.combo_interfacespeed.addItem("1000000")

        self.combo_fd_interfacespeed = QComboBox(self)
        self.combo_fd_interfacespeed.addItem("1000000")
        self.combo_fd_interfacespeed.addItem("2000000")
        self.combo_fd_interfacespeed.addItem("5000000")


        button_connect = QPushButton("&Connect", self)
        button_disconnect = QPushButton("&Disconnect", self)
        send_frame = QPushButton("&SEND", self)
        receive_frame = QPushButton("&RECEIVE", self)

        self.comm_to_send = QLineEdit(self)
        self.comm_to_send.setInputMask('HH-HH-HH-HH-HH-HH-HH-HH')

        ukladT = QGridLayout()
        ukladT.addWidget(label_interfacetype, 0, 0)
        ukladT.addWidget(self.combo_interfacetype, 0, 1)
        ukladT.addWidget(label_interfacechannel, 1, 0)
        ukladT.addWidget(self.combo_interfacechannel, 1, 1)
        ukladT.addWidget(label_interfacespeed, 2, 0)
        ukladT.addWidget(self.combo_interfacespeed, 2, 1)
        ukladT.addWidget(label_fd_interfacespeed, 3, 0)
        ukladT.addWidget(self.combo_fd_interfacespeed, 3, 1)
        ukladT.addWidget(button_connect, 4, 1)
        ukladT.addWidget(button_disconnect, 5, 1)
        ukladT.addWidget(self.text_interfacetype, 6, 1)
        ukladT.addWidget(send_frame, 7, 0)
        ukladT.addWidget(self.comm_to_send, 7, 1)
        ukladT.addWidget(receive_frame, 8, 0)


        self.tab1.setLayout(ukladT)

        button_connect.clicked.connect(self.CAN_conf)
        button_disconnect.clicked.connect(self.CAN_disconf)
        send_frame.clicked.connect(self.send_COMM)
        receive_frame.clicked.connect(self.receive_COMM)

        self.setGeometry(20, 20, 600, 600)
        self.setWindowTitle("Dzida Laserowa #<--->#             beta 0.0")
        self.show()

    def CAN_conf(self):
            CAN_type = bool(self.combo_interfacetype.currentIndex())
            CAN_channel = self.combo_interfacechannel.currentIndex()
            CAN_bitrate = int(self.combo_interfacespeed.currentText())
            CAN_data_bitrate = int(self.combo_fd_interfacespeed.currentText())

            self.CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=[0xCA, 0x50, 0x01], extended_id=True, is_fd=True)
            self.text_interfacetype.insertPlainText("sent:  CA 50 01\n")
            self.CAN_msg2 = can.Message(arbitration_id=0x18DA0000, data=[0xCA, 0x50, 0x02], extended_id=True)
            self.text_interfacetype.insertPlainText("sent:  CA 50 02\n")
            self.CAN_msg3 = can.Message(arbitration_id=0x18DA0000, data=[0xCA, 0x50, 0x03], extended_id=True)
            self.text_interfacetype.insertPlainText("sent:  CA 50 03\n")

            self.CAN_bus = VectorBus(channel=CAN_channel, bitrate=CAN_bitrate, fd=CAN_type, data_bitrate=CAN_data_bitrate, receive_own_messages=False)
            #        CAN_type = int(self.text_interfacetype.text())
            print(str(CAN_type) + '  ' + str(CAN_channel) + '  ' + str(CAN_bitrate) + ' ' + str(CAN_data_bitrate))
            self.text_interfacetype.insertPlainText(
                "konfiguracja CAN_CASE  " + str(CAN_type) + '  ' + str(CAN_channel) + '  ' + str(CAN_bitrate)+ ' ' + str(CAN_data_bitrate) + "\n")
            try:
                self.CAN_bus.send(self.CAN_msg1)
            except can.CanError:
                print("Message not sent")

            #        self.timer.start(1000)
         #   CAN_rtmsg = self.CAN_bus.recv(0.1)
         #   self.text_interfacetype.insertPlainText("received" + str(CAN_rtmsg) + "\n")
         #   CAN_rtmsg = self.CAN_bus.recv(0.1)
         #   self.text_interfacetype.insertPlainText("received" + str(CAN_rtmsg) + "\n")
         #   CAN_rtmsg = self.CAN_bus.recv(0.1)
         #   self.text_interfacetype.insertPlainText("received" + str(CAN_rtmsg) + "\n")

    def CAN_disconf(self):
            #        CAN_received = []
            #        CAN_received.append({0x54, 0x56, 0x67, 0x87})
            #        CAN_received.append({0x54, 0x56, 0x67, 0x87})
            #        CAN_received.append({0x54, 0x56, 0x67, 0x87})
            #        CAN_received.append({0x54, 0x56, 0x67, 0x87})
            #        self.text_interfacetype.insertPlainText("received po zakonczeniu " + str(CAN_received) + "\n")
            #self.timer.stop()
            self.CAN_bus.shutdown()

    def send_COMM(self):
        command4 = []
        print("command sent")
        self.text_interfacetype.insertPlainText("command sent\n")
        self.io_comm = self.comm_to_send.text()
        self.text_interfacetype.insertPlainText(self.io_comm +'\n')
        command = list(self.io_comm)
        self.text_interfacetype.insertPlainText(str(command) +'\n')
        command2 = list(self.io_comm.split('-'))
        self.text_interfacetype.insertPlainText(str(command2) + '\n')
#        command3 = list(map(int,command2))
#        self.text_interfacetype.insertPlainText(str(command3) + '\n')
        for i in range(len(command2)):
            if command2[i] != str(''):
                command4.append(int(command2[i],16))
        self.text_interfacetype.insertPlainText(str(command4) + '\n')

        print(self.io_comm)
        #        self.CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=[0x31, 0x01, 0x14, 0x00, 0x00, 0x0A, 0x07, 0x01], extended_id=True)
        self.CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=[0x02, 0x3E, 0x00], extended_id=True, is_fd=True, bitrate_switch=True)
        self.CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=command4, extended_id=True, is_fd=True, bitrate_switch=True)
        #self.CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=[0x31, 0x01, 0x14, 0x00, 0x00, 0x02, 0x0F, 0x01], extended_id=True, is_fd=True, bitrate_switch=True)
        #self.CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=[0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA, 0xAA], extended_id=True, is_fd=True, bitrate_switch=True)
        #        self.CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=[0x31, 0x01, 0x1B, 0x00, 0x02, 0x00, 0x19], extended_id=True)
        try:
            self.CAN_bus.send(self.CAN_msg1)
        except can.CanError:
            print("Message not sent")
        self.text_interfacetype.insertPlainText("sent: " + str(self.CAN_msg1) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.1)
        self.text_interfacetype.insertPlainText("received" + str(CAN_rtmsg) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.1)
        self.text_interfacetype.insertPlainText("received" + str(CAN_rtmsg) + "\n")

    def receive_COMM(self):
        CAN_rtmsg = self.CAN_bus.recv(0.1)
        self.text_interfacetype.insertPlainText("received" + str(CAN_rtmsg) + "\n")


if __name__=='__main__':

    app=QApplication(sys.argv)
    okno=Diagnostyk()
    sys.exit(app.exec_())
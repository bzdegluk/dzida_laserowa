import sys
import csv
import can, struct
from can.interfaces.vector.canlib import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread, Qt
from time import sleep
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QTabWidget, QPlainTextEdit, QProgressBar, QScrollBar, QSlider
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout, QVBoxLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout

class Diagnostyk(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.addTab(self.tab1, "CAN CONFIG")
        self.addTab(self.tab2, "HCP1 CONTROL")

        self.interfejs()
        self.interfejs2()

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
        self.combo_interfacechannel.setCurrentIndex(1)

        self.combo_interfacespeed = QComboBox(self)
        self.combo_interfacespeed.addItem("100000")
        self.combo_interfacespeed.addItem("250000")
        self.combo_interfacespeed.addItem("500000")
        self.combo_interfacespeed.addItem("1000000")
        self.combo_interfacespeed.setCurrentIndex(2)

        self.combo_fd_interfacespeed = QComboBox(self)
        self.combo_fd_interfacespeed.addItem("1000000")
        self.combo_fd_interfacespeed.addItem("2000000")
        self.combo_fd_interfacespeed.addItem("5000000")
        self.combo_fd_interfacespeed.setCurrentIndex(1)


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

#        self.setGeometry(20, 20, 600, 600)
#        self.setWindowTitle("Dzida Laserowa #<--->#             beta 0.0")
#        self.show()

# Druga zakladka

    def interfejs2(self):
        label_SetGPIO = QLabel("Set GPIO", self)
        labe_SetPWM = QLabel("Set PWM freq and duty",self)
        label_ReadADC = QLabel("Read ADC value",self)
        label_BuildDate = QLabel("Core IO build Date",self)

        button_gpio_set = QPushButton("&Set GPIO",self)
        button_gpio_reset = QPushButton("&Reset GPIO",self)
        button_pmw_set = QPushButton("&PWM SET")
        button_adc_get = QPushButton("&Read ADC")
        button_sleep = QPushButton("&Go to Sleep")
        button_test = QPushButton("Tester Present")


        self.gpio_comm = QLineEdit(self)
        self.gpio_comm.setInputMask('999-99')
        self.pwm_freq = QLineEdit(self)
        self.pwm_freq.setText("25")
#        self.pwm_freq.setInputMask('999999')
        self.pwm_duty = QLineEdit(self)
        self.pwm_duty.setText("50")
#        self.pwm_duty.setInputMask('999')
        self.adc_value = QLineEdit(self)
        self.test_result = QLineEdit(self)
        self.build_date = QLineEdit(self)

        self.text_interfacetype_2 = QPlainTextEdit()


        self.combo_pwm_chanell = QComboBox(self)
        self.combo_pwm_chanell.addItem("LSD_1A")
        self.combo_pwm_chanell.addItem("Damper_1A")
        self.combo_pwm_chanell.addItem("LSD_1B")
        self.combo_pwm_chanell.addItem("Damper_1B")
        self.combo_pwm_chanell.addItem("LSD_2A")
        self.combo_pwm_chanell.addItem("Damper_2A")
        self.combo_pwm_chanell.addItem("LSD_2B")
        self.combo_pwm_chanell.addItem("Damper_2B")
        self.combo_pwm_chanell.addItem("LSD_3A")
        self.combo_pwm_chanell.addItem("Damper_3A")
        self.combo_pwm_chanell.addItem("LSD_3B")
        self.combo_pwm_chanell.addItem("Damper_3B")
        self.combo_pwm_chanell.addItem("LSD_4A")
        self.combo_pwm_chanell.addItem("Damper_4A")
        self.combo_pwm_chanell.addItem("LSD_4B")
        self.combo_pwm_chanell.addItem("Damper_4B")
        self.combo_pwm_chanell.addItem("Force_FB_Acc_Pedal")
        self.combo_adc_chanell = QComboBox(self)
        self.combo_adc_chanell.addItem("Damper1B_fb")
        self.combo_adc_chanell.addItem("Damper1B_P_FB")
        self.combo_adc_chanell.addItem("Damper1B_N_FB")
        self.combo_adc_chanell.addItem("Master_Aurix_KL15_Sense")
        self.combo_adc_chanell.addItem("SENT_2_supply")
        self.combo_adc_chanell.addItem("Damper2A_fb")
        self.combo_adc_chanell.addItem("Damper2A_N_FB")
        self.combo_adc_chanell.addItem("Damper2A_P_FB")
        self.combo_adc_chanell.addItem("SENT_1_supply")
        self.combo_adc_chanell.addItem("SBC_AMUX")
        self.combo_adc_chanell.addItem("Damper2B_fb")
        self.combo_adc_chanell.addItem("Damper2B_P_FB")
        self.combo_adc_chanell.addItem("Damper2B_N_FB")
        self.combo_adc_chanell.addItem("PF_AMUX")
        self.combo_adc_chanell.addItem("RCAR_MAIN_SUPPLY_PGOOD")
        self.combo_adc_chanell.addItem("Damper3A_fb")
        self.combo_adc_chanell.addItem("SENSE_HSD_VBAT_DAMPER")
        self.combo_adc_chanell.addItem("KL30A_2_VOLT")
        self.combo_adc_chanell.addItem("Damper3A_N_FB")
        self.combo_adc_chanell.addItem("Damper3A_P_FB")
        self.combo_adc_chanell.addItem("Damper3B_fb")
        self.combo_adc_chanell.addItem("Damper3B_P_FB")
        self.combo_adc_chanell.addItem("Damper4B_P_FB")
        self.combo_adc_chanell.addItem("Damper3B_N_FB")
        self.combo_adc_chanell.addItem("Pedal_Low_FB")
        self.combo_adc_chanell.addItem("Damper4B_N_FB")
        self.combo_adc_chanell.addItem("KL30A_1_Curr")
        self.combo_adc_chanell.addItem("Damper_LSD_ERR")
        self.combo_adc_chanell.addItem("Reserved do not use")
        self.combo_adc_chanell.addItem("KL30A_2_Curr")
        self.combo_adc_chanell.addItem("Damper4B_fb")
        self.combo_adc_chanell.addItem("Damper1A_fb")
        self.combo_adc_chanell.addItem("Damper1A_N_FB")
        self.combo_adc_chanell.addItem("Damper1A_P_FB")
        self.combo_adc_chanell.addItem("Damper4A_fb")
        self.combo_adc_chanell.addItem("Damper4A_N_FB")
        self.combo_adc_chanell.addItem("TEMP_VREF")
        self.combo_adc_chanell.addItem("BLS")
        self.combo_adc_chanell.addItem("KL30A_1_VOLT")
        self.combo_adc_chanell.addItem("Damper4A_P_FB")
        self.combo_adc_chanell.addItem("Force_FB_Acc_Pedal")
        self.combo_adc_chanell.addItem("FORCE_FB_SENSE")
        self.combo_adc_chanell.addItem("Master_Aurix_KL15_Sense2")

#        self.combo_gpio_port = QComboBox(self)
#        self.combo_gpio_port.addItem("DO_SREG_OUT_ENABLE")
#        self.combo_gpio_port.addItem("Master_Aurix_Power_EN")
#        self.combo_gpio_port.addItem("Force_FB_Acc_Pedal_DIAG_EN")
#        self.combo_gpio_port.addItem("Force_FB_Acc_Pedal_EN")
#        self.combo_gpio_port.addItem("DO_BLS_PU_enable")
#        self.combo_gpio_port.addItem("CAN3_EN")
#        horiz_group_1 = QHBoxLayout()
#        horiz_group_1.addWidget(button_test,0)
#        horiz_group_1.addWidget(self.test_result, 0)
#        horiz_group_1.addWidget(self.build_date, 0)

        ukladT2 = QGridLayout()
        ukladT2.addWidget(button_test,0 ,0)
        ukladT2.addWidget(self.test_result, 0, 1)
        ukladT2.addWidget(self.build_date, 0, 2)
        ukladT2.addWidget(label_BuildDate, 0, 3)
        ukladT2.addWidget(label_SetGPIO,1,0)
        ukladT2.addWidget(self.gpio_comm,1,1)
        ukladT2.addWidget(button_gpio_set,1,2)
        ukladT2.addWidget(button_gpio_reset,1,3)
        ukladT2.addWidget(labe_SetPWM,2,0)
        ukladT2.addWidget(self.combo_pwm_chanell,2,1)
        ukladT2.addWidget(self.pwm_duty, 2, 2)
        ukladT2.addWidget(self.pwm_freq,2,3)
        ukladT2.addWidget(button_pmw_set,2,4)
        ukladT2.addWidget(label_ReadADC,3,0)
        ukladT2.addWidget(self.combo_adc_chanell,3,1)
        ukladT2.addWidget(button_adc_get,3,2)
        ukladT2.addWidget(self.adc_value,3,3)
        ukladT2.addWidget(button_sleep,4,0)
        ukladT2.addWidget(self.text_interfacetype_2, 5, 0, 1, 5)

#        layout = QVBoxLayout()
#        layout.addWidget(horiz_group_1)
#        layout.addWidget(ukladT2)
#        self.tab2.setLayout(horiz_group_1)
        self.tab2.setLayout(ukladT2)

        button_gpio_set.clicked.connect(self.GPIO_set)
        button_gpio_reset.clicked.connect(self.GPIO_reset)
        button_pmw_set.clicked.connect(self.send_PWM_Set)
        button_adc_get.clicked.connect(self.send_ADC_Read)
        button_sleep.clicked.connect(self.send_Go_Sleep)
        button_test.clicked.connect(self.send_Test)

        self.setGeometry(20, 20, 600, 600)
        self.setWindowTitle("Dzida Laserowa #<--->#             beta 0.3")
        self.move(150, 150)
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
            CAN_rtmsg2 = self.CAN_bus.recv(0.1)
            self.CAN_bus.flush_tx_buffer()
#            while CAN_rtmsg2 != None:
#            while len(CAN_rtmsg2.data) > 0:
#                CAN_rtmsg2 = self.CAN_bus.recv(0.1)
            print("dodone")

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
#        CAN_rtmsg = self.CAN_bus.recv(0.1)
#        self.text_interfacetype.insertPlainText("received" + str(CAN_rtmsg) + "\n")
        CAN_rtmsg2 = self.CAN_bus.recv(0.1)
#        while CAN_rtmsg2 != None:
#            CAN_rtmsg2 = self.CAN_bus.recv(0.1)

    def receive_COMM(self):

        CAN_rtmsg = self.CAN_bus.recv(0.1)
        self.text_interfacetype.insertPlainText("received" + str(CAN_rtmsg) + "\n")

    def GPIO_set(self):
        self.send_GPIO_Set(True)
        print ("hello")


    def GPIO_reset(self):
        self.send_GPIO_Set(False)

    def send_GPIO_Set(self, state):
        self.gpio_command = self.gpio_comm.text()
        command_gpio_t = list(self.gpio_command.split('-'))
        print (command_gpio_t)
        command_gpio = [0x10, 0x08, 0x31, 0x01, 0x14, 0x00, 0x00]
        command_gpio.append(int(command_gpio_t[0],10))
        command_gpio2 = [0x21]
        command_gpio2.append(int(command_gpio_t[1],10))
#        command_gpio2.append(int(command_gpio_t[2], 10))
        if state == True:
            command_gpio2.append(0x01)
        else:
            command_gpio2.append(0x00)
        command_gpio2.append(0x00)
        command_gpio2.append(0x00)
        command_gpio2.append(0x00)
        command_gpio2.append(0x00)
        command_gpio2.append(0x00)

        print (command_gpio)
        print (command_gpio2)
        self.CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=command_gpio, extended_id=True, is_fd=True, bitrate_switch=True)
        self.CAN_msg2 = can.Message(arbitration_id=0x18DA0000, data=command_gpio2, extended_id=True, is_fd=True, bitrate_switch=True)
        try:
            self.CAN_bus.send(self.CAN_msg1)
        except can.CanError:
            print("Message not sent")
        self.text_interfacetype_2.insertPlainText("sent: " + str(self.CAN_msg1) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.1)
        self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
        try:
            self.CAN_bus.send(self.CAN_msg2)
        except can.CanError:
            print("Message not sent")
        self.text_interfacetype_2.insertPlainText("sent: " + str(self.CAN_msg2) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.1)
        self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
        CAN_rtmsg2 = self.CAN_bus.recv(0.1)
#        while CAN_rtmsg2 != None:
#            CAN_rtmsg2 = self.CAN_bus.recv(0.1)

    def send_PWM_Set(self):
        channel = self.combo_pwm_chanell.currentIndex()
        duty = int(self.pwm_duty.text())
        freq = int(self.pwm_freq.text())
        print(str(channel) + ' ' + str(freq) + ' ' + str(duty))
        command_pwm = [0x07, 0x31, 0x01, 0x1B, 0x00]
        command_pwm.append(channel)
        command_pwm.append(duty)
        command_pwm.append(freq >> 24)
        command_pwm.append((freq )>> 24)
        print (command_pwm)

        CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=command_pwm, extended_id=True, is_fd=True, bitrate_switch=True)

        try:
            self.CAN_bus.send(CAN_msg1)
        except can.CanError:
            print("Message not sent")
        self.text_interfacetype_2.insertPlainText("sent: " + str(CAN_msg1) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.1)
        self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
        CAN_rtmsg2 = self.CAN_bus.recv(0.1)
        while CAN_rtmsg2 != None:
            CAN_rtmsg2 = self.CAN_bus.recv(0.1)

    def send_ADC_Read(self):
        channel = self.combo_adc_chanell.currentIndex()
        command_adc = [0x06, 0x31, 0x01, 0x1A, 0x02, 0x00]
        command_adc.append(channel)
        print (command_adc)

        CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=command_adc, extended_id=True, is_fd=True, bitrate_switch=True)

        try:
            self.CAN_bus.send(CAN_msg1)
        except can.CanError:
            print("Message not sent")
        self.text_interfacetype_2.insertPlainText("sent: " + str(CAN_msg1) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.1)
        self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
        self.text_interfacetype_2.moveCursor(QtGui.QTextCursor.End)

#        print (CAN_rtmsg)
        if len(CAN_rtmsg.data) != 0:
            if CAN_rtmsg.data[1] == 0x71:
#                self.adc_value.setText(str(CAN_rtmsg.data[5])+str(CAN_rtmsg.data[6]))
                self.adc_value.setText(str((CAN_rtmsg.data[5]*256)+CAN_rtmsg.data[6]))
        CAN_rtmsg2 = self.CAN_bus.recv(0.1)
        while CAN_rtmsg2 != None:
            CAN_rtmsg2 = self.CAN_bus.recv(0.1)

    def send_Go_Sleep(self):
        CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=[0x04,0x31, 0x01, 0xFF, 0xA0], extended_id=True, is_fd=True, bitrate_switch=True)

        try:
            self.CAN_bus.send(CAN_msg1)
        except can.CanError:
            print("Message not sent")
        self.text_interfacetype_2.insertPlainText("sent: " + str(CAN_msg1) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.1)
        self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
        self.CAN_bus.flush_tx_buffer()
        CAN_rtmsg2 = self.CAN_bus.recv(0.1)
        while CAN_rtmsg2 != None:
            CAN_rtmsg2 = self.CAN_bus.recv(0.1)

    def send_Test(self):
        CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=[0x02, 0x3E, 0x00], extended_id=True, is_fd=True, bitrate_switch=True)

        try:
            self.CAN_bus.send(CAN_msg1)
        except can.CanError:
            print("Message not sent")
        self.text_interfacetype_2.insertPlainText("sent: " + str(CAN_msg1) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.1)
        self.text_interfacetype_2.insertPlainText("received: " + str(CAN_rtmsg) + "\n")

        if len(CAN_rtmsg.data) != 0:
            if CAN_rtmsg.data[1] == 0x7E:
                self.test_result.setText("Module Connected")
                CAN_rtmsg2 = self.CAN_bus.recv(0.1)
                while CAN_rtmsg2 != None:
                    CAN_rtmsg2 = self.CAN_bus.recv(0.1)
                CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=[0x03, 0x22, 0x10, 0x10], extended_id=True, is_fd=True, bitrate_switch=True)

                try:
                    self.CAN_bus.send(CAN_msg1)
                except can.CanError:
                    print("Message not sent")
                self.text_interfacetype_2.insertPlainText("sent: " + str(CAN_msg1) + "\n")
                self.text_interfacetype_2.moveCursor(QtGui.QTextCursor.End)
                CAN_rtmsg = self.CAN_bus.recv(0.1)
                self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
                self.text_interfacetype_2.moveCursor(QtGui.QTextCursor.End)

                if len(CAN_rtmsg.data) != 0:
                    if CAN_rtmsg.data[2] == 0x62:
                        self.build_date.setText(str(CAN_rtmsg.data[5])+'-'+str(CAN_rtmsg.data[6])+'-20'+str(CAN_rtmsg.data[7]))
#                        print("nothing")
                    else:
                        self.build_date.clear()
                CAN_rtmsg2 = self.CAN_bus.recv(0.1)
                while CAN_rtmsg2 != None:
                    CAN_rtmsg2 = self.CAN_bus.recv(0.1)

            else:
                self.test_result.setText("Module Not available")




if __name__=='__main__':

    app=QApplication(sys.argv)
    okno=Diagnostyk()
#    w = QtGui.QWidget()
#    tryicon = QtWidgets.QSystemTrayIcon(QtGui.QIcon('dzida.jpg'), w)
#    tryicon.show()
    app.setWindowIcon(QtGui.QIcon('dzida.jpg'))
    app.setStyle('Fusion')
    sys.exit(app.exec_())
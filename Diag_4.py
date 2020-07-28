import sys
import csv
from UDS import UDS
from UDS import *
import can, struct
from can.interfaces.vector.canlib import *
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread, Qt
from time import sleep
from PyQt5.QtWidgets import QApplication, QWidget, QComboBox, QTabWidget, QPlainTextEdit, QProgressBar, QScrollBar, QSlider, QMainWindow, QGroupBox
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout, QVBoxLayout
from PyQt5.QtWidgets import QLineEdit, QPushButton, QHBoxLayout
from PyQt5.QtCore import QSize, QRegExp
from PyQt5.QtGui import QRegExpValidator
import socket
import pickle

# new refresh for GIT test

frame = {
    "timestamp" : 0.0,
    "arbitration_id" : 0x18DA0000,
    "extended_id" : True,
    "is_remote_frame" : False,
    "is_error_frame" : False,
    "channel" : None,
    "dlc" : None,
    "data" : None,
    "is_fd": True,
    "bitrate_switch" : True,
    "error_state_indicator" : False,
    "extended_id" : True,
    "check" : False
}

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(20, 20, 800, 800)
        self.move(60, 60)
        self.setWindowTitle("Dzida Laserowa #<--->#             beta 1.0")

        self.text_int = QPlainTextEdit()
        self.text_int.insertPlainText("CAN interface disconnected ... \n")
        wind_lay = QVBoxLayout()
        self.group = QGroupBox()
        main_uklad = QGridLayout()
        tab_widget = Diagnostyk(self, window=self.text_int)
#        self.setCentralWidget(self.tab_widget)
#        self.text_int = QPlainTextEdit()
        label_interfacetype = QLabel("CAN Interface Type", self)
#        self.setCentralWidget(self.text_int)
        main_uklad.addWidget(tab_widget, 0, 0)
        main_uklad.addWidget(self.text_int, 1, 0)
        main_uklad.addWidget(label_interfacetype, 2, 0)
        self.group.setLayout(main_uklad)
#        wind_lay.addWidget(self.group)
#        self.setLayout(main_uklad)
        self.setCentralWidget(self.group)

        self.show()

class Diagnostyk(QTabWidget):
    def __init__(self, parent, window):
        super().__init__(parent)

        self.window = window
#        self.window.insertPlainText("  dupa2")

        self.uds = UDS()

        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
#        self.text_int = QPlainTextEdit()

        self.addTab(self.tab1, "CAN CONFIG")
        self.addTab(self.tab2, "HCP1 CONTROL")
        self.addTab(self.tab3, "RASPI CAN")


        self.interfejs()
        self.interfejs2()
        self.interfejs3()

#        self.comm_to_send.setText([0x31, 0x01, 0xFC, 0x02, 0x0E, 0x00, 0x02, 0x18, 0x00])
        self.comm_to_send.setText("31-01-FC-02-0E-00-02-18-00")

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
        self.combo_interfacechannel.addItem("3")
        self.combo_interfacechannel.addItem("4")
        self.combo_interfacechannel.addItem("5")
        self.combo_interfacechannel.addItem("6")
        self.combo_interfacechannel.addItem("7")
        self.combo_interfacechannel.addItem("8")
        self.combo_interfacechannel.addItem("9")
        self.combo_interfacechannel.addItem("10")
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
#        send_new = QPushButton("&Send2", self)
        sweep = QPushButton("SWEEP", self)


        self.comm_to_send = QLineEdit(self)
        self.comm_to_send.setInputMask('HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH-HH')


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
        ukladT.addWidget(sweep, 9, 0)


        self.tab1.setLayout(ukladT)

        button_connect.clicked.connect(self.CAN_conf)
        button_disconnect.clicked.connect(self.CAN_disconf)
        send_frame.clicked.connect(self.send_COMM)
        receive_frame.clicked.connect(self.receive_COMM)
        sweep.clicked.connect(self.Sweep_comm)

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
        button_spi = QPushButton("Send SPI")


#        self.gpio_comm = QLineEdit(self)
#        self.gpio_comm.setInputMask('999-99')
        self.pwm_freq = QLineEdit(self)
        self.pwm_freq.setText("25000")
#        self.pwm_freq.setInputMask('999999')
        self.pwm_duty = QLineEdit(self)
        self.pwm_duty.setText("50")
#        self.pwm_duty.setInputMask('999')
        self.adc_value = QLineEdit(self)
        self.test_result = QLineEdit(self)
        self.build_date = QLineEdit(self)
        self.spi_command_trans = QLineEdit(self)
        self.spi_command_receiv = QLineEdit(self)

        self.text_interfacetype_2 = QPlainTextEdit()

        self.gpio_comm = QComboBox(self)
        self.gpio_comm.addItems(list(self.uds.gpios))

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
        ukladT2.addWidget(button_spi,4,0)
        ukladT2.addWidget(self.spi_command_trans,4,1)
        ukladT2.addWidget(self.spi_command_receiv,5,1)
        ukladT2.addWidget(button_sleep,6,0)
        ukladT2.addWidget(self.text_interfacetype_2, 7, 0, 1, 5)

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
        button_spi.clicked.connect(self.send_SPI)

# Trzecia zakladka

    def interfejs3(self):

        label_SetGPIO = QLabel("Set GPIO", self)

        button_gpio_set2 = QPushButton("&Set GPIO", self)
        button_gpio_reset2 = QPushButton("&Reset GPIO", self)
        button_rpi_connect = QPushButton("RPI_Connect", self)
        button_rpi_disconnect = QPushButton("RPI_Disconnect", self)

        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"  # Part of the regular expression
        # Regulare expression
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)

        self.gpio_comm2 = QLineEdit(self)
        self.gpio_comm2.setInputMask('999-99')
        self.RPI_IP = QLineEdit(self)
        self.RPI_IP.setValidator(ipValidator)
        self.RPI_IP.setText('192.168.8.104')

        ukladT3 = QGridLayout()
        ukladT3.addWidget(label_SetGPIO, 1, 0)
        ukladT3.addWidget(self.gpio_comm2, 1, 1)
        ukladT3.addWidget(button_gpio_set2, 1, 2)
        ukladT3.addWidget(button_gpio_reset2, 1, 3)
        ukladT3.addWidget(button_rpi_connect, 2, 1)
        ukladT3.addWidget(self.RPI_IP, 2, 2)
        ukladT3.addWidget(button_rpi_disconnect, 3, 0)
        self.tab3.setLayout(ukladT3)

        button_gpio_set2.clicked.connect(self.GPIO_set)
        button_gpio_reset2.clicked.connect(self.GPIO_reset)
        button_rpi_connect.clicked.connect(self.RPI_connect)
        button_rpi_disconnect.clicked.connect(self.RPI_disconnect)


#        self.setGeometry(20, 20, 600, 600)
#        self.move(150, 150)
#        self.show()


    def CAN_conf(self):
            CAN_type = bool(self.combo_interfacetype.currentIndex())
            CAN_channel = self.combo_interfacechannel.currentIndex()
            CAN_bitrate = int(self.combo_interfacespeed.currentText())
            CAN_data_bitrate = int(self.combo_fd_interfacespeed.currentText())
            CAN_interface = "Vector"


#            self.uds = UDS()
            self.uds.mess_win_conf(self.window)
            self.uds_can = self.uds.CAN_config(CAN_interface, CAN_type, CAN_channel, CAN_bitrate, CAN_data_bitrate)

#            self.uds.CAN_send([0x3E, 0x00])

            print(str(CAN_type) + '  ' + str(CAN_channel) + '  ' + str(CAN_bitrate) + ' ' + str(CAN_data_bitrate))
            self.text_interfacetype.insertPlainText(
                "konfiguracja CAN_CASE  " + str(CAN_type) + '  ' + str(CAN_channel) + '  ' + str(CAN_bitrate)+ ' ' + str(CAN_data_bitrate) + "\n")



    def CAN_disconf(self):
        self.uds.CAN_disconfig()

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
        rec = self.uds.CAN_send(command4)
#        print(rec)
#        self.uds_Send(command4)

    def receive_COMM(self):

        CAN_rtmsg = self.CAN_bus.recv(0.1)
        self.text_interfacetype.insertPlainText("received" + str(CAN_rtmsg) + "\n")

    def GPIO_set(self):
#        self.send_GPIO_Set(True)

        self.uds.uds_gpio_set(self.gpio_comm.currentText(), True)
        print ("hello")


    def GPIO_reset(self):
        self.uds.uds_gpio_set(self.gpio_comm.currentText(), False)
        print ("hello")

#    def GPIO2_reset(self):

    def send_PWM_Set(self):
        channel = self.combo_pwm_chanell.currentIndex()
        duty = int(self.pwm_duty.text())
        freq = int(self.pwm_freq.text())
#       0x31 0x01 0x1B 0x00 chanel duty freq freq freq freq 0x00 0x00 0x00
        command_pwm = [0x31, 0x01, 0x1B, 0x00]
        command_pwm.append(channel)
        command_pwm.append(duty)
        command_pwm.append(freq >> 24)
        command_pwm.append((freq & 0xFFFFFF) >> 16)
        command_pwm.append((freq & 0xFFFF) >> 8)
        command_pwm.append(freq & 0xFF)
        print(str(channel) + ' ' + str(freq) + ' ' + str(duty))

        rec = self.uds.CAN_send(command_pwm)

    def send_ADC_Read(self):
        channel = self.combo_adc_chanell.currentIndex()
#       0x31 0x01 0x1A 0x02 0x00 channel

        command_adc = [0x31, 0x01, 0x1A, 0x02, 0x00]
        command_adc.append(channel)

        rec = self.uds.CAN_send(command_adc)
        print(command_adc)

        if rec[0] is not None:
            if len(rec[0].data) != 0:
                if rec[0].data[1] == 0x71:
                    self.adc_value.setText(str((rec[0].data[5]*256)+rec[0].data[6]))


    def send_Go_Sleep(self):
        rec = self.uds.CAN_send([0x31, 0x01, 0xFF, 0xA0])

    def send_Test(self):

        rec = self.uds.CAN_send([0x3E, 0x00])

        if len(rec[0].data) != 0:
            if rec[0].data[1] == 0x7E:
                self.test_result.setText("Module Connected")
                rec = self.uds.CAN_send([0x22, 0x10, 0x10])
                if rec[0] is not None:
                    if len(rec[0].data) != 0:
                        if rec[0].data[2] == 0x62:
                            self.build_date.setText(str(rec[0].data[5])+'-'+str(rec[0].data[6])+'-20'+str(rec[0].data[7]))
#                            print("nothing")
                        else:
                            self.build_date.clear()

            else:
                self.test_result.setText("Module Not available")

    def RPI_connect(self):
#        header = 'dzida   '

#        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = self.RPI_IP.text()
        print(address)
        s.connect((address, 1235))

    def RPI_disconnect(self):
        s.close()

    def GPIO2_reset(self):
        header2 = 'dzida   '
        frame2 = 'taka sytuacja'
        print(header2+str(len(frame2))+frame2)
        s.send(bytes(header2+str(len(frame2))+frame2, "utf-8"))
#        s.send(bytes(frame2, "utf-8"))

    def uds_Send(self, uds_command):
        arbit_ID = 0x18DA0000
        messages = []
        cnt = 0

        if len(uds_command) < 8:
            uds_command.insert(0, (len(uds_command)))
            messages[0] = can.Message(arbitration_id=0x18DA0000, data=uds_command, extended_id=True, is_fd=True, bitrate_switch=True)
            cnt = 1
        else:
            for x in range((((len(uds_command))//7)+1)):
                temp = messages[(x * 7):((x * 7) + 7)]
                temp.insert(0, (0x21 + x))
                messages[x] = can.Message(arbitration_id=0x18DA0000, data=temp, extended_id=True, is_fd=True, bitrate_switch=True)
                self.text_interfacetype_2.insertPlainText("sent: " + str(messages[x]) + "\n")
                cnt += 1

#        for mess in messages:
#            try:
#                self.CAN_bus.send(mess)
#            except can.CanError:
#                print("Message not sent")
#            CAN_rtmsg = self.CAN_bus.recv(0.1)
#            if CAN_rtmsg is not None:
#                self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
#            self.text_interfacetype_2.moveCursor(QtGui.QTextCursor.End)
    def Sweep_comm(self):

        sweep = []

#        self.CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=[0x10, 0x14, 0x31, 0x01, 0x1B, 0x01, 0x00, 0x00], extended_id=True, is_fd=True, bitrate_switch=True)
#        self.CAN_msg2 = can.Message(arbitration_id=0x18DA0000, data=[0x21, 0x75, 0x30, 0x00, 0x00, 0x9C, 0x40, 0x00], extended_id=True, is_fd=True, bitrate_switch=True)
#        self.CAN_msg3 = can.Message(arbitration_id=0x18DA0000, data=[0x22, 0x00, 0x01, 0xF4, 0x00, 0x00, 0x00, 0x05], extended_id=True, is_fd=True, bitrate_switch=True)

#        self.CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=[0x10, 0x14, 0x31, 0x01, 0x1B, 0x01, 0x00, 0x00],
#                                    extended_id=True, is_fd=True, bitrate_switch=True)
#        self.CAN_msg2 = can.Message(arbitration_id=0x18DA0000, data=[0x21, 0x00, 0x00, 0x00, 0x00, 0x0, 0x00, 0x00],
#                                    extended_id=True, is_fd=True, bitrate_switch=True)
#        self.CAN_msg3 = can.Message(arbitration_id=0x18DA0000, data=[0x22, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
#                                    extended_id=True, is_fd=True, bitrate_switch=True)

#       31 01 1B 01 00 00 0F A0 00 00 17 70 00 00 00 2D 00 00 00 01  - 4k do 6k co 45
#       31 01 1B 01 00 00 4E 20 00 00 75 A8 00 00 00 E6 00 00 00 01  - 20kHz do 30120Hz co 230
#       31 01 1B 01 00 00 13 88 00 00 1B 58 00 00 00 2D 00 00 00 01  - 5k do 7k co 45

#        self.CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=[0x10, 0x14, 0x31, 0x01, 0x1B, 0x01, 0x00, 0x00],
#                                    extended_id=True, is_fd=True, bitrate_switch=True)
#        self.CAN_msg2 = can.Message(arbitration_id=0x18DA0000, data=[0x21, 0x4E, 0x20, 0x00, 0x00, 0x75, 0xA8, 0x00],
#                                    extended_id=True, is_fd=True, bitrate_switch=True)
#        self.CAN_msg3 = can.Message(arbitration_id=0x18DA0000, data=[0x22, 0x00, 0x00, 0xE6, 0x00, 0x00, 0x00, 0x01],
#                                    extended_id=True, is_fd=True, bitrate_switch=True)


#           I2C check

#        self.CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=[0x10, 0x0D, 0x31, 0x01, 0x17, 0x03, 0x00, 0x07],
#                                    extended_id=True, is_fd=True, bitrate_switch=True)
#        self.CAN_msg2 = can.Message(arbitration_id=0x18DA0000, data=[0x21, 0x00, 0x60, 0x00, 0x01, 0x00, 0x01, 0x3E],
#                                    extended_id=True, is_fd=True, bitrate_switch=True)
#        self.CAN_msg3 = can.Message(arbitration_id=0x18DA0000, data=[0x04, 0x31, 0x03, 0x17, 0x03],
#                                    extended_id=True, is_fd=True, bitrate_switch=True)

        self.CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=[0x04, 0x31, 0x01, 0x17, 0x06], extended_id=True, is_fd=True, bitrate_switch=True)
        self.CAN_msg2 = can.Message(arbitration_id=0x18DA0000, data=[0x04, 0x31, 0x03, 0x17, 0x06],
                                    extended_id=True, is_fd=True, bitrate_switch=True)
        self.CAN_msg3 = can.Message(arbitration_id=0x18DA0000, data=[0x30, 0x00, 0x0A],
                                    extended_id=True, is_fd=True, bitrate_switch=True)

#        self.CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=[0x10, 0x31, 0x03, 0x17, 0x05, 0x00],
#                                    extended_id=True, is_fd=True, bitrate_switch=True)

        try:
            self.CAN_bus.send(self.CAN_msg1)
        except can.CanError:
            print("Message not sent")

        self.text_interfacetype_2.insertPlainText("sent: " + str(self.CAN_msg1) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.1)
        if CAN_rtmsg is not None:
            self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")

        sleep(1.0)

        try:
            self.CAN_bus.send(self.CAN_msg2)
        except can.CanError:
            print("Message not sent")
        self.text_interfacetype_2.insertPlainText("sent: " + str(self.CAN_msg2) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.1)
        if CAN_rtmsg is not None:
            self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
            try:
                self.CAN_bus.send(self.CAN_msg3)
            except can.CanError:
                print("Message not sent")
            self.text_interfacetype_2.insertPlainText("sent: " + str(self.CAN_msg3) + "\n")

        CAN_rtmsg2 = self.CAN_bus.recv(0.1)
        if CAN_rtmsg2 is not None:
            self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg2) + "\n")
        self.text_interfacetype_2.moveCursor(QtGui.QTextCursor.End)

#        sleep(0.1)
#        try:
#           self.CAN_bus.send(self.CAN_msg3)
#        except can.CanError:
#            print("Message not sent")
#        self.text_interfacetype_2.insertPlainText("sent: " + str(self.CAN_msg3) + "\n")
#        CAN_rtmsg = self.CAN_bus.recv(0.1)
#        if CAN_rtmsg is not None:
#            self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
#        CAN_rtmsg2 = self.CAN_bus.recv(0.1)
#        self.text_interfacetype_2.moveCursor(QtGui.QTextCursor.End)
#        self.uds_Send(sweep)

    def send_SPI(self):

        self.CAN_msg1 = can.Message(arbitration_id=0x18DA0000, data=[0x10, 0x09, 0x31, 0x01, 0xFC, 0x02, 0x0E, 0x00],
                                    extended_id=True, is_fd=True, bitrate_switch=True)
        self.CAN_msg2 = can.Message(arbitration_id=0x18DA0000, data=[0x21, 0x02, 0x55, 0x55, 0x00, 0x00, 0x00, 0x00],
                                    extended_id=True, is_fd=True, bitrate_switch=True)
        self.CAN_msg3 = can.Message(arbitration_id=0x18DA0000, data=[0x22, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                                    extended_id=True, is_fd=True, bitrate_switch=True)
        self.CAN_msg4 = can.Message(arbitration_id=0x18DA0000, data=[0x23, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                                    extended_id=True, is_fd=True, bitrate_switch=True)
        self.CAN_msg5 = can.Message(arbitration_id=0x18DA0000, data=[0x24, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                                    extended_id=True, is_fd=True, bitrate_switch=True)
        self.CAN_msg6 = can.Message(arbitration_id=0x18DA0000, data=[0x25, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                                    extended_id=True, is_fd=True, bitrate_switch=True)
        self.CAN_msg7 = can.Message(arbitration_id=0x18DA0000, data=[0x26, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                                    extended_id=True, is_fd=True, bitrate_switch=True)
        self.CAN_msg8 = can.Message(arbitration_id=0x18DA0000, data=[0x27, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                                    extended_id=True, is_fd=True, bitrate_switch=True)
        self.CAN_msg9 = can.Message(arbitration_id=0x18DA0000, data=[0x28, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00],
                                    extended_id=True, is_fd=True, bitrate_switch=True)
        self.CAN_msg10 = can.Message(arbitration_id=0x18DA0000, data=[0x2A, 0x00, 0x00],
                                    extended_id=True, is_fd=True, bitrate_switch=True)


        try:
            self.CAN_bus.send(self.CAN_msg1)
        except can.CanError:
            print("Message not sent")

        self.text_interfacetype_2.insertPlainText("sent: " + str(self.CAN_msg1) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.2)
        if CAN_rtmsg is not None:
            self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")

        try:
            self.CAN_bus.send(self.CAN_msg2)
        except can.CanError:
            print("Message not sent")
        self.text_interfacetype_2.insertPlainText("sent: " + str(self.CAN_msg2) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.2)
        if CAN_rtmsg is not None:
            self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
        CAN_rtmsg2 = self.CAN_bus.recv(0.2)
        self.text_interfacetype_2.moveCursor(QtGui.QTextCursor.End)
'''
        try:
            self.CAN_bus.send(self.CAN_msg3)
        except can.CanError:
            print("Message not sent")
        self.text_interfacetype_2.insertPlainText("sent: " + str(self.CAN_msg3) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.2)
        if CAN_rtmsg is not None:
            self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
        CAN_rtmsg2 = self.CAN_bus.recv(0.1)
        self.text_interfacetype_2.moveCursor(QtGui.QTextCursor.End)
        try:
            self.CAN_bus.send(self.CAN_msg4)
        except can.CanError:
            print("Message not sent")
        self.text_interfacetype_2.insertPlainText("sent: " + str(self.CAN_msg4) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.2)
        if CAN_rtmsg is not None:
            self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
        CAN_rtmsg2 = self.CAN_bus.recv(0.1)
        self.text_interfacetype_2.moveCursor(QtGui.QTextCursor.End)

        try:
            self.CAN_bus.send(self.CAN_msg5)
        except can.CanError:
            print("Message not sent")
        self.text_interfacetype_2.insertPlainText("sent: " + str(self.CAN_msg5) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.2)
        if CAN_rtmsg is not None:
            self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
        CAN_rtmsg2 = self.CAN_bus.recv(0.1)
        self.text_interfacetype_2.moveCursor(QtGui.QTextCursor.End)

        try:
            self.CAN_bus.send(self.CAN_msg6)
        except can.CanError:
            print("Message not sent")
        self.text_interfacetype_2.insertPlainText("sent: " + str(self.CAN_msg6) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.2)
        if CAN_rtmsg is not None:
            self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
        CAN_rtmsg2 = self.CAN_bus.recv(0.1)
        self.text_interfacetype_2.moveCursor(QtGui.QTextCursor.End)

        try:
            self.CAN_bus.send(self.CAN_msg7)
        except can.CanError:
            print("Message not sent")
        self.text_interfacetype_2.insertPlainText("sent: " + str(self.CAN_msg7) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.2)
        if CAN_rtmsg is not None:
            self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
        CAN_rtmsg2 = self.CAN_bus.recv(0.1)
        self.text_interfacetype_2.moveCursor(QtGui.QTextCursor.End)

        try:
            self.CAN_bus.send(self.CAN_msg8)
        except can.CanError:
            print("Message not sent")
        self.text_interfacetype_2.insertPlainText("sent: " + str(self.CAN_msg8) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.2)
        if CAN_rtmsg is not None:
            self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
        CAN_rtmsg2 = self.CAN_bus.recv(0.1)
        self.text_interfacetype_2.moveCursor(QtGui.QTextCursor.End)

        try:
            self.CAN_bus.send(self.CAN_msg9)
        except can.CanError:
            print("Message not sent")
        self.text_interfacetype_2.insertPlainText("sent: " + str(self.CAN_msg9) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.2)
        if CAN_rtmsg is not None:
            self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
        CAN_rtmsg2 = self.CAN_bus.recv(0.1)
        self.text_interfacetype_2.moveCursor(QtGui.QTextCursor.End)

        try:
            self.CAN_bus.send(self.CAN_msg10)
        except can.CanError:
            print("Message not sent")
        self.text_interfacetype_2.insertPlainText("sent: " + str(self.CAN_msg10) + "\n")
        CAN_rtmsg = self.CAN_bus.recv(0.2)
        if CAN_rtmsg is not None:
            self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
        CAN_rtmsg2 = self.CAN_bus.recv(0.1)
        self.text_interfacetype_2.moveCursor(QtGui.QTextCursor.End)
'''

if __name__=='__main__':

    app=QApplication(sys.argv)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    okno = App()
#    okno=Diagnostyk()
#    w = QtGui.QWidget()
#    tryicon = QtWidgets.QSystemTrayIcon(QtGui.QIcon('dzida.jpg'), w)
#    tryicon.show()
    app.setWindowIcon(QtGui.QIcon('dzida.jpg'))
    app.setStyle('Fusion')
    sys.exit(app.exec_())
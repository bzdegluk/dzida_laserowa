import can, struct
from can.interfaces.vector.canlib import *
from PyQt5 import QtGui
from time import sleep

class UDS:
    gpios = {
        "DO_FRAYB0_RESET": [0, 2],
        "DO_FRAYB1_RESET": [0, 5],
        "DI_FRAY_INTA": [0, 11],
        "DO_SLAVE_WD": [0, 12],
        "FRAYA_ATXEN": [2, 4],
        "FRAYB_ATXEN": [2, 5],
        "DO_SREG_OUT_ENABLE": [2, 6],
        "DI_FRAY_INTB": [2, 7],
        "DO_FRAY_LWUA": [10, 0],
        "DO_FRAY_BGEA": [10, 1],
        "Master_Aurix_Power_EN": [10, 3],
        "DO_Power_Force_FB_Acc_Pedal_DIAG_EN": [10, 4],
        "DO_Power_Force_FB_Acc_Pedal_EN": [10, 7],
        "MDC": [12, 0],
        "MDIO": [12, 1],
        "DO_FRAYA1_RESET": [13, 0],
        "ETH_ON_3V3": [15, 0],
        "DO_ETH_PHY_RST": [15, 4],
        "DO_FRAY_LWUB": [15, 8],
        "DO_SBC_WAKE_EN": [20, 1],
        "Master_Aurix_3V3": [20, 2],
        "Slave_Aurix_Power_RST": [21, 0],
        "DO_SREG_MR": [21, 1],
        "DO_PSI5_EN": [22, 4],
        "DI_SENT_5V_ERR": [22, 5],
        "DI_Master_Aurix_Power_INT": [22, 6],
        "DI_Master_Aurix_Power_Safe_State": [22, 7],
        "DO_SENT_5V_1_EN": [22, 11],
        "DO_SENT_5V_2_EN": [23, 3],
        "DO_FRAY_BGEB": [23, 7],
        "DO_Force_Acc_Pedal_diag_EN": [32, 0],
        "MASTER_2_SLAVE_CTRL_2": [32, 1],
        "DO_HSD_VBAT_DAMPER": [32, 4],
        "DO_ETH_PHY_WAKE_IN": [32, 5],
        "MASTER_2_SLAVE_CTRL_1": [32, 6],
        "DO_SW_RST": [32, 7],
        "DI_Master_Aurix_Power_ERR": [33, 8],
        "DO_LIN_nSLP": [33, 14],
        "DO_BOOST_ENABLE": [33, 15],
        "DO_FRAYA0_RESET": [34, 4],
        "DO_REV_BAT_SLEEP": [34, 5],
        "DI_Damper_ERR": [40, 4],
        "DO_CAN_1_EN": [252, 0],
        "DO_CAN_2_EN": [252, 1],
        "DO_CAN_3_EN": [252, 2],
        "DO_CAN_4_EN": [252, 3],
        "DO_CAN_5_EN": [252, 4],
        "DO_CAN_6_EN": [252, 5],
        "DO_CAN_7_EN": [252, 6],
        "DO_CAN_8_EN": [252, 7],
        "DO_CAN_WU_EN": [253, 0],
        "DO_CAN_1_nSTB": [253, 1],
        "DO_CAN_2_nSTB": [253, 2],
        "DO_CAN_WU_nSTB": [253, 3],
        "DO_CAN_4_nSTB": [253, 4],
        "DO_CAN_5_nSTB": [253, 5],
        "DO_CAN_6_nSTB": [253, 6],
        "DO_CAN_7_nSTB": [253, 7],
        "DO_CAN_8_nSTB": [254, 0],
        "DO_CAN_3_nSTB": [254, 1],
        "DO_Damper_Driver1_EN": [254, 2],
        "DO_Damper_Driver2_EN": [254, 3],
        "DO_Damper_Driver3_EN": [254, 4],
        "DO_Damper_Driver4_EN": [254, 5],
        "RCAR_PRESETn_3V3": [254, 6],
        "DO_RCAR_MAIN_EN": [254, 7]
    }
    def mess_win_conf(self, mess_window):
        self.mess_window = mess_window
#        self.mess_window.insertPlainText("  dupa3")

    def CAN_config(self, UDS_CAN_interface, UDS_CAN_type, UDS_CAN_channel, UDS_CAN_bitrate,  UDS_CAN_data_bitrate):
        try:
            self.config_stat = True
            self.CAN_bus = VectorBus(channel=UDS_CAN_channel, bitrate=UDS_CAN_bitrate, fd=UDS_CAN_type, data_bitrate=UDS_CAN_data_bitrate,
                            receive_own_messages=False)
        except can.CanError as error:
            print(error)
            print("CAN interface could not be connected, HW unavailable... \n")
            self.mess_window.insertPlainText("CAN interface could not be connected, HW unavailable... \n")
            self.mess_window.moveCursor(QtGui.QTextCursor.End)
            self.config_stat = False

        if self.config_stat is not False:
            self.mess_window.insertPlainText("CAN interface connected ... \n")
            self.mess_window.insertPlainText(str(self.CAN_bus) + "\n\n")
            self.mess_window.moveCursor(QtGui.QTextCursor.End)
            return self.CAN_bus
        else:
            return None

    def CAN_disconfig(self):
        self.mess_window.insertPlainText("CAN interface disconnected \n")
        self.CAN_bus.shutdown()


    def CAN_send(self, uds_command):
        arbit_ID = 0x18DA0000
        messages = []
        rec_mess = []
        cnt = 0
        flow_cc = can.Message(arbitration_id=0x18DA0000, data=[0x30, 0x00, 0x0A], extended_id=True, is_fd=True,
                                      bitrate_switch=True)

        if len(uds_command) < 8:
            temp = [len(uds_command)]
            temp.extend(uds_command[0:(len(uds_command))])
            messages.append(can.Message(arbitration_id=0x18DA0000, data=temp, extended_id=True, is_fd=True,
                                      bitrate_switch=True))
            cnt = 1
        else:
            temp = [0x10]
            temp.append(len(uds_command))
            temp.extend(uds_command[0:6])
            messages.append(can.Message(arbitration_id=0x18DA0000, data=temp, extended_id=True, is_fd=True,
                                      bitrate_switch=True))
            for x in range(1, (((len(uds_command)) // 7) + 1)):
                temp = []
                temp.insert(0, (0x21 + (x-1)))
                temp.extend(uds_command[((x * 7)-1):((x * 7) + 6)])

                if x == ((len(uds_command)) // 7):
                    for z in range(len(temp),8):
                        temp.append(0x00)

                messages.append(can.Message(arbitration_id=0x18DA0000, data=temp, extended_id=True, is_fd=True, bitrate_switch=True))
#                self.text_interfacetype_2.insertPlainText("sent: " + str(messages[x]) + "\n")
                cnt += 1

#        for x in range(len(messages[len(messages)-1]),8):
#            messages[len(messages)-1].append(0x00)

        for mess in messages:
            print(str(mess))

        if self.config_stat is not False:
            for mess in messages:
                try:
                    self.CAN_bus.send(mess)
                except can.CanError:
                    print("Message not sent")
                self.mess_window.insertPlainText("Sent: " + str(mess) + '\n')
                CAN_rtmsg = self.CAN_bus.recv(0.01)
                if CAN_rtmsg is not None:
                    rec_mess.append(CAN_rtmsg)
                    print(CAN_rtmsg)
                    self.CAN_bus.send(flow_cc)
                    print("flow_cc")
                    self.mess_window.insertPlainText("Received: " + str(CAN_rtmsg) + "\n")
#                   self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
#                   self.text_interfacetype_2.moveCursor(QtGui.QTextCursor.End)

                self.mess_window.insertPlainText("\n")
                self.mess_window.moveCursor(QtGui.QTextCursor.End)
                print ("data 0 = " + str(CAN_rtmsg.data[0]))
                if CAN_rtmsg.data[0] == 16:
                    CAN_rtmsg = self.CAN_bus.recv(0.01)
                    if CAN_rtmsg is not None:
                        rec_mess.append(CAN_rtmsg)
                        print(CAN_rtmsg)
                        self.mess_window.insertPlainText("Received: " + str(CAN_rtmsg) + "\n")
                        #                   self.text_interfacetype_2.insertPlainText("received" + str(CAN_rtmsg) + "\n")
                        #                   self.text_interfacetype_2.moveCursor(QtGui.QTextCursor.End)
                        self.CAN_bus.send(flow_cc)
                    self.mess_window.insertPlainText("\n")
                    self.mess_window.moveCursor(QtGui.QTextCursor.End)
                print ("dupa")
#                sleep(0.2)
            return rec_mess
        else:
            self.mess_window.insertPlainText("Message could no be sent due to missing CAN interface")
            self.mess_window.moveCursor(QtGui.QTextCursor.End)
            return None

    def uds_gpio_set(self, gpio, level):
        print(self.gpios[gpio][0])
        command_gpio = [0x31, 0x01, 0x14, 0x00, 0x00]
        command_gpio.append(self.gpios[gpio][0])
        command_gpio.append(self.gpios[gpio][1])
        if level == True:
            command_gpio.append(0x01)
        else:
            command_gpio.append(0x00)
        print(command_gpio)
        self.CAN_send(command_gpio)



#        try:
#            self.CAN_bus.send(UDS_message)
#        except can.CanError:
#            print("Message not sent")
#        CAN_rtmsg = self.CAN_bus.recv(0.1)
#        uds_can.flush_tx_buffer()
#        return CAN_rtmsg


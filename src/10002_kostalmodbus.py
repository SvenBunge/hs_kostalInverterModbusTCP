# coding: UTF-8
import logging
import pymodbus  # To not delete this module reference!!
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient

##!!!!##################################################################################################
#### Own written code can be placed above this commentblock . Do not change or delete commentblock! ####
########################################################################################################
##** Code created by generator - DO NOT CHANGE! **##

class Kostalmodbus10002(hsl20_3.BaseModule):

    def __init__(self, homeserver_context):
        hsl20_3.BaseModule.__init__(self, homeserver_context, "kostalmodbus10002")
        self.FRAMEWORK = self._get_framework()
        self.LOGGER = self._get_logger(hsl20_3.LOGGING_NONE,())
        self.PIN_I_TRIGGER=1
        self.PIN_I_TIME_CURRENT_POWER_VALUES=2
        self.PIN_I_INVERTER_IP=3
        self.PIN_I_PORT=4
        self.PIN_I_UNIT_ID=5
        self.PIN_O_BATTERY_SOC=1
        self.PIN_O_HOME_CONSUMPTION_BATTERY=2
        self.PIN_O_HOME_CONSUMPTION_GRID=3
        self.PIN_O_HOME_CONSUMPTION_PV=4
        self.PIN_O_HOME_CONSUMPTION_TOTAL=5
        self.PIN_O_TOTAL_POWER_FROM_GRID=6
        self.PIN_O_TOTAL_POWER_FROM_PV=7
        self.PIN_O_INVERTER_POWER=8
        self.PIN_O_POWER_FROM_BATTERY=9
        self.FRAMEWORK._run_in_context_thread(self.on_init)

########################################################################################################
#### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
###################################################################################################!!!##

        self.DEBUG = self.FRAMEWORK.create_debug_section()

        self.holdingRegister = {
            "batterySOC": ['u16', 514, self.PIN_O_BATTERY_SOC, 0],
            "batteryCONSUMPTION": ['f32', 106, self.PIN_O_HOME_CONSUMPTION_BATTERY, 0.0],
            "gridCONSUMPTION": ['f32', 108, self.PIN_O_HOME_CONSUMPTION_GRID, 0.0],
            "pvCONSUMPTION": ['f32', 116, self.PIN_O_HOME_CONSUMPTION_PV, 0.0],
            "gridPOWER": ['f32', 252, self.PIN_O_TOTAL_POWER_FROM_GRID, 0.0],
            "inverterPOWER": ['f32', 575, self.PIN_O_INVERTER_POWER, 0.0],
            "batteryPOWER": ['s16', 582, self.PIN_O_POWER_FROM_BATTERY, 0]
        }

#############

    def read_current_power_values(self, ip_address, port_number, unit_id):
        client = None
        try:
            self.DEBUG.set_value("creating client with IP:", ip_address)
            self.DEBUG.set_value("creating client with Port:", port_number)
            self.DEBUG.set_value("creating client with UnitID:", unit_id)
            client = ModbusTcpClient(ip_address, port=port_number)
            client.connect()

            self.read_power_values(client, unit_id)
        finally:
            if client:
                client.close()

    def read_power_values(self, client, unit_id):

        # fetch all registers
        for register in self.holdingRegister:
            value = 0
            if self.holdingRegister[register][0] == 'u16':
                value = Kostalmodbus10002.read_u16_1(client, unit_id, self.holdingRegister[register][1])
            elif self.holdingRegister[register][0] == 's16':
                value = Kostalmodbus10002.read_s16_1(client, unit_id, self.holdingRegister[register][1])
            elif self.holdingRegister[register][0] == 'f32':
                value = Kostalmodbus10002.read_32float_2(client, unit_id, self.holdingRegister[register][1])

            self.DEBUG.set_value(register, value)  # set Debug value
            self._set_output_value(self.holdingRegister[register][2], value)  # set value to output PIN
            self.holdingRegister[register][3] = value  # assign value to variable

        # Calculate current total home consumption
        total_consumption = self.holdingRegister['batteryCONSUMPTION'][3] + self.holdingRegister['gridCONSUMPTION'][3] + self.holdingRegister['pvCONSUMPTION'][3]
        self.DEBUG.set_value('totalCONSUMPTION', total_consumption)
        self._set_output_value(self.PIN_O_HOME_CONSUMPTION_TOTAL, total_consumption)

        # Calculate total power from PV
        total_power_from_pv = min(0, self.holdingRegister['batteryPOWER'][3]) + min(0, self.holdingRegister['gridPOWER'][3]) + self.holdingRegister['pvCONSUMPTION'][3]
        self.DEBUG.set_value('pvPOWER', total_power_from_pv)
        self._set_output_value(self.PIN_O_TOTAL_POWER_FROM_PV, total_power_from_pv)

    #############

    def on_init(self):
        pass

    def on_input_value(self, index, value):
        if index == self.PIN_I_TRIGGER:
            ip_address = str(self._get_input_value(self.PIN_I_INVERTER_IP))
            port = int(self._get_input_value(self.PIN_I_PORT))
            unit_id = int(self._get_input_value(self.PIN_I_UNIT_ID))
            self.read_current_power_values(ip_address, port, unit_id)


    @staticmethod
    def read_u16_1(client, unit_id, reg_addr):
        result = client.read_holding_registers(reg_addr, 1, unit=unit_id)
        if not result.isError():
            return BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big,
                                                  wordorder=Endian.Little).decode_16bit_uint()
        else:
            return -1

    @staticmethod
    def read_s16_1(client, unit_id, reg_addr):
        result = client.read_holding_registers(reg_addr, 1, unit=unit_id)
        if not result.isError():
            return BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big,
                                                  wordorder=Endian.Little).decode_16bit_int()
        else:
            return -1

    @staticmethod
    def read_32float_2(client, unit_id, reg_addr):
        result = client.read_holding_registers(reg_addr, 2, unit=unit_id)
        if not result.isError():
            return BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big,
                                                  wordorder=Endian.Little).decode_32bit_float()
        else:
            return -1

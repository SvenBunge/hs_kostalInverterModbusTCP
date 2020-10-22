# coding: UTF-8
import pymodbus  # To not delete this module reference!!
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient

##!!!!##################################################################################################
#### Own written code can be placed above this commentblock . Do not change or delete commentblock! ####
########################################################################################################
##** Code created by generator - DO NOT CHANGE! **##

class Kostalmodbus14180(hsl20_3.BaseModule):

    def __init__(self, homeserver_context):
        hsl20_3.BaseModule.__init__(self, homeserver_context, "kostalmodbus14180")
        self.FRAMEWORK = self._get_framework()
        self.LOGGER = self._get_logger(hsl20_3.LOGGING_NONE,())
        self.PIN_I_SWITCH=1
        self.PIN_I_FETCH_INTERVAL=2
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
        self.PIN_O_TOTAL_YIELD=10
        self.PIN_O_DAILY_YIELD=11
        self.PIN_O_MONTHLY_YIELD=12
        self.PIN_O_YEARLY_YIELD=13
        self.FRAMEWORK._run_in_context_thread(self.on_init)

########################################################################################################
#### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
###################################################################################################!!!##

        self.interval = None
        self.DEBUG = self.FRAMEWORK.create_debug_section()

        self.total_consumption_sbc, self.total_power_from_pv_sbc = (-1, ) * 2

        self.holdingRegister = {
            "batterySOC": ['u16', 514, self.PIN_O_BATTERY_SOC, 0, None],
            "batteryCONSUMPTION": ['f32', 106, self.PIN_O_HOME_CONSUMPTION_BATTERY, 0.0, None],
            "gridCONSUMPTION": ['f32', 108, self.PIN_O_HOME_CONSUMPTION_GRID, 0.0, None],
            "pvCONSUMPTION": ['f32', 116, self.PIN_O_HOME_CONSUMPTION_PV, 0.0, None],
            "gridPOWER": ['f32', 252, self.PIN_O_TOTAL_POWER_FROM_GRID, 0.0, None],
            "inverterPOWER": ['f32', 575, self.PIN_O_INVERTER_POWER, 0.0, None],
            "batteryPOWER": ['s16', 582, self.PIN_O_POWER_FROM_BATTERY, 0, None],
            "totalYIELD": ['f32', 320, self.PIN_O_TOTAL_YIELD, 0.0, lambda x: x / 1000],
            "dailyYIELD": ['f32', 322, self.PIN_O_DAILY_YIELD, 0.0, lambda x: x / 1000],
            "monthlyYIELD": ['f32', 326, self.PIN_O_MONTHLY_YIELD, 0.0, lambda x: x / 1000],
            "yearlyYIELD": ['f32', 324, self.PIN_O_YEARLY_YIELD, 0.0, lambda x: x / 1000]
        }

#############

    def on_interval(self):
        ip_address = str(self._get_input_value(self.PIN_I_INVERTER_IP))
        port = int(self._get_input_value(self.PIN_I_PORT))
        unit_id = int(self._get_input_value(self.PIN_I_UNIT_ID))

        client = None
        try:
            self.DEBUG.set_value("creating client with IP:", ip_address)
            self.DEBUG.set_value("creating client with Port:", port)
            self.DEBUG.set_value("creating client with UnitID:", unit_id)
            client = ModbusTcpClient(ip_address, port)
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
                value = Kostalmodbus14180.read_u16_1(client, unit_id, self.holdingRegister[register][1])
            elif self.holdingRegister[register][0] == 's16':
                value = Kostalmodbus14180.read_s16_1(client, unit_id, self.holdingRegister[register][1])
            elif self.holdingRegister[register][0] == 'f32':
                value = Kostalmodbus14180.read_32float_2(client, unit_id, self.holdingRegister[register][1])

            self.DEBUG.set_value(register, value)  # set Debug raw value

            # apply lambda if set
            if self.holdingRegister[register][4] is not None:
                value = self.holdingRegister[register][4](value)

            self._set_output_value(self.holdingRegister[register][2], value)  # set value to output PIN

            # send by change if check (sbc)
            if self.holdingRegister[register][3] != value:
                self.holdingRegister[register][3] = value  # assign value to variable

        # Calculate current total home consumption
        total_consumption = self.holdingRegister['batteryCONSUMPTION'][3] + self.holdingRegister['gridCONSUMPTION'][3] + self.holdingRegister['pvCONSUMPTION'][3]
        if self.total_consumption_sbc != total_consumption:
            self.DEBUG.set_value('totalCONSUMPTION', total_consumption)
            self._set_output_value(self.PIN_O_HOME_CONSUMPTION_TOTAL, total_consumption)
            self.total_consumption_sbc = total_consumption

        # Calculate total power from PV
        total_power_from_pv = -1 * (min(0, self.holdingRegister['batteryPOWER'][3]) + min(0, self.holdingRegister['gridPOWER'][3])) + self.holdingRegister['pvCONSUMPTION'][3]
        if self.total_power_from_pv_sbc != total_power_from_pv:
            self.DEBUG.set_value('pvPOWER', total_power_from_pv)
            self._set_output_value(self.PIN_O_TOTAL_POWER_FROM_PV, total_power_from_pv)
            self.total_power_from_pv_sbc = total_power_from_pv

    #############

    def on_init(self):
        self.interval = self.FRAMEWORK.create_interval()
        if self._get_input_value(self.PIN_I_SWITCH) == 1:
            self.interval.set_interval(self._get_input_value(self.PIN_I_FETCH_INTERVAL) * 1000, self.on_interval)
            self.interval.start()

    def on_input_value(self, index, value):
        if index == self.PIN_I_SWITCH:
            self.interval.stop()
            if value == 1:
                self.interval.set_interval(self._get_input_value(self.PIN_I_FETCH_INTERVAL) * 1000, self.on_interval)
                self.interval.start()

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

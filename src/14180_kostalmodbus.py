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
        self.PIN_I_MODBUS_ENDIAN=6
        self.PIN_O_HOME_CONSUMPTION_BATTERY=1
        self.PIN_O_HOME_CONSUMPTION_GRID=2
        self.PIN_O_HOME_CONSUMPTION_PV=3
        self.PIN_O_HOME_CONSUMPTION_TOTAL=4
        self.PIN_O_TOTAL_POWER_FROM_GRID=5
        self.PIN_O_TOTAL_POWER_FROM_PV=6
        self.PIN_O_INVERTER_POWER=7
        self.PIN_O_INVERTER_STATE_INT=8
        self.PIN_O_INVERTER_STATE=9
        self.PIN_O_POWER_FROM_BATTERY=10
        self.PIN_O_TOTAL_YIELD=11
        self.PIN_O_DAILY_YIELD=12
        self.PIN_O_MONTHLY_YIELD=13
        self.PIN_O_YEARLY_YIELD=14
        self.PIN_O_DC1_VOLTAGE=15
        self.PIN_O_DC1_CURRENT=16
        self.PIN_O_DC2_VOLTAGE=17
        self.PIN_O_DC2_CURRENT=18
        self.PIN_O_DC3_VOLTAGE=19
        self.PIN_O_DC3_CURRENT=20
        self.PIN_O_BATTERY_SOC=21
        self.PIN_O_BATTERY_CYCLES=22
        self.PIN_O_BATTERY_VOLTAGE=23
        self.PIN_O_BATTERY_TEMPERATURE=24
        self.PIN_O_BATTERY_READY=25
        self.FRAMEWORK._run_in_context_thread(self.on_init)

########################################################################################################
#### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
###################################################################################################!!!##

        self.interval = None
        self.DEBUG = self.FRAMEWORK.create_debug_section()

        self.total_consumption_sbc, self.total_power_from_pv_sbc, self.inverter_state = (-1, ) * 3

        self.holdingRegister = {
            "batterySOC": ['f32', 210, self.PIN_O_BATTERY_SOC, 0, None],
            "batteryCycles": ['f32', 194, self.PIN_O_BATTERY_CYCLES, 0, None],
            "batteryVoltage": ['f32', 216, self.PIN_O_BATTERY_VOLTAGE, 0.0, None],
            "batteryTemperature": ['f32', 214, self.PIN_O_BATTERY_TEMPERATURE, 0.0, None],
            "batteryConsumption": ['f32', 106, self.PIN_O_HOME_CONSUMPTION_BATTERY, 0, None],
            "batteryReady": ['f32', 208, self.PIN_O_BATTERY_READY, 0, None],
            "gridConsumption": ['f32', 108, self.PIN_O_HOME_CONSUMPTION_GRID, 0, None],
            "pvConsumption": ['f32', 116, self.PIN_O_HOME_CONSUMPTION_PV, 0, None],
            "gridPower": ['f32', 252, self.PIN_O_TOTAL_POWER_FROM_GRID, 0, None],
            "inverterPower": ['f32', 575, self.PIN_O_INVERTER_POWER, 0, None],
            "inverterStateInt": ['u16', 56, self.PIN_O_INVERTER_STATE_INT, 0, None],
            "batteryPower": ['s16', 582, self.PIN_O_POWER_FROM_BATTERY, 0, None],
            "totalYield": ['f32', 320, self.PIN_O_TOTAL_YIELD, 0.0, lambda x: x / 1000],
            "dailyYield": ['f32', 322, self.PIN_O_DAILY_YIELD, 0.0, lambda x: x / 1000],
            "monthlyYield": ['f32', 326, self.PIN_O_MONTHLY_YIELD, 0.0, lambda x: x / 1000],
            "yearlyYield": ['f32', 324, self.PIN_O_YEARLY_YIELD, 0.0, lambda x: x / 1000],
            "dc1_voltage": ['f32', 266, self.PIN_O_DC1_VOLTAGE, 0.0, None],
            "dc1_current": ['f32', 258, self.PIN_O_DC1_CURRENT, 0.0, None],
            "dc2_voltage": ['f32', 276, self.PIN_O_DC2_VOLTAGE, 0.0, None],
            "dc2_current": ['f32', 268, self.PIN_O_DC2_CURRENT, 0.0, None],
            "dc3_voltage": ['f32', 286, self.PIN_O_DC3_VOLTAGE, 0.0, None],
            "dc3_current": ['f32', 278, self.PIN_O_DC3_CURRENT, 0.0, None]
        }

        self.inverter_State_Mapping = ["Off", "Init", "IsoMeas", "Grid Check", "Start Up", "-", "Feed In", "Throttled",
                                       "Ext. Switch Off", "Update", "Standby", "Grid Sync", "Grid Pre-Check",
                                       "Grid Switch Off", "Overheating", "Shutdown", "Inproper DC Voltage!", "ESB", "Unknown"]

#############

    def on_interval(self):
        ip_address = str(self._get_input_value(self.PIN_I_INVERTER_IP))
        port = int(self._get_input_value(self.PIN_I_PORT))
        unit_id = int(self._get_input_value(self.PIN_I_UNIT_ID))

        client = None
        try:
            self.DEBUG.set_value("Connection IP:Port (UnitID)", ip_address + ":" + str(port) + " (" + str(unit_id) + ") ")
            client = ModbusTcpClient(ip_address, port)
            client.connect()

            self.read_power_values(client, unit_id)
        except Exception as err:
            self.DEBUG.set_value("Last exception msg logged", err.message)
            raise
        finally:
            if client:
                client.close()

    def read_power_values(self, client, unit_id):

        # fetch all registers
        for register in self.holdingRegister:
            value = 0
            if self.holdingRegister[register][0] == 'u16':
                value = self.read_u16_1(client, unit_id, self.holdingRegister[register][1])
            elif self.holdingRegister[register][0] == 's16':
                value = self.read_s16_1(client, unit_id, self.holdingRegister[register][1])
            elif self.holdingRegister[register][0] == 'f32':
                value = self.read_32float_2(client, unit_id, self.holdingRegister[register][1])

            self.DEBUG.set_value(register, value)  # set Debug raw value

            # apply lambda if set
            if self.holdingRegister[register][4] is not None:
                value = self.holdingRegister[register][4](value)

            self._set_output_value(self.holdingRegister[register][2], value)  # set value to output PIN

            # send by change if check (sbc)
            if self.holdingRegister[register][3] != value:
                self.holdingRegister[register][3] = value  # assign value to variable

        # Calculate current total home consumption
        total_consumption = self.holdingRegister['batteryConsumption'][3] + self.holdingRegister['gridConsumption'][3] + self.holdingRegister['pvConsumption'][3]
        if self.total_consumption_sbc != total_consumption:
            self.DEBUG.set_value('totalConsumption', total_consumption)
            self._set_output_value(self.PIN_O_HOME_CONSUMPTION_TOTAL, total_consumption)
            self.total_consumption_sbc = total_consumption

        # Calculate total power from PV
        total_power_from_pv = -1 * (min(0, self.holdingRegister['batteryPower'][3]) + min(0, self.holdingRegister['gridPower'][3])) + self.holdingRegister['pvConsumption'][3]
        if self.total_power_from_pv_sbc != total_power_from_pv:
            self.DEBUG.set_value('pvPower', total_power_from_pv)
            self._set_output_value(self.PIN_O_TOTAL_POWER_FROM_PV, total_power_from_pv)
            self.total_power_from_pv_sbc = total_power_from_pv

        inverter_state = self.getInverterString(self.holdingRegister['inverterStateInt'][3])
        if self.inverter_state != inverter_state:
            self._set_output_value(self.PIN_O_INVERTER_STATE, inverter_state)
            self.inverter_state = inverter_state

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

    def read_u16_1(self, client, unit_id, reg_addr):
        result = client.read_holding_registers(reg_addr, 1, unit=unit_id)
        if not result.isError():
            return BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big,
                                                  wordorder=self.getWordOrder()).decode_16bit_uint()
        else:
            return -1

    def read_s16_1(self, client, unit_id, reg_addr):
        result = client.read_holding_registers(reg_addr, 1, unit=unit_id)
        if not result.isError():
            return BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big,
                                                  wordorder=self.getWordOrder()).decode_16bit_int()
        else:
            return -1

    def read_32float_2(self, client, unit_id, reg_addr):
        result = client.read_holding_registers(reg_addr, 2, unit=unit_id)
        if not result.isError():
            return BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big,
                                                  wordorder=self.getWordOrder()).decode_32bit_float()
        else:
            return -1

    def getWordOrder(self):
        if int(self._get_input_value(self.PIN_I_UNIT_ID)) == 1:
            return Endian.Big
        else:
            return Endian.Little

    #############

    def getInverterString(self, inverter_status_int):
        if 0 <= inverter_status_int < len(self.inverter_State_Mapping):
            return self.inverter_State_Mapping[inverter_status_int]
        else:
            return "---"

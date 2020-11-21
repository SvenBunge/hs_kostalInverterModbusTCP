# coding: UTF-8

import pymodbus  # To not delete this module reference!!
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient

##!!!!##################################################################################################
#### Own written code can be placed above this commentblock . Do not change or delete commentblock! ####
########################################################################################################
##** Code created by generator - DO NOT CHANGE! **##

class KostalWR_modbusTCP14180(hsl20_3.BaseModule):

    def __init__(self, homeserver_context):
        hsl20_3.BaseModule.__init__(self, homeserver_context, "kostalWRmodbusTCP14180")
        self.FRAMEWORK = self._get_framework()
        self.LOGGER = self._get_logger(hsl20_3.LOGGING_NONE,())
        self.PIN_I_SWITCH=1
        self.PIN_I_FETCH_INTERVAL=2
        self.PIN_I_INVERTER_IP=3
        self.PIN_I_PORT=4
        self.PIN_I_UNIT_ID=5
        self.PIN_I_MODBUS_ENDIAN=6
        self.PIN_I_BATTERY_AT_DC3=7
        self.PIN_I_TOTAL_SUM_REGISTERS_EXISTS=8
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
        self.PIN_O_TOTAL_DC_CHARGE_ENERGY=26
        self.PIN_O_TOTAL_DC_DISCHARGE_ENERGY=27
        self.PIN_O_TOTAL_AC_CHARGE_ENERGY=28
        self.PIN_O_TOTAL_AC_DISCHARGE_ENERGY=29
        self.PIN_O_TOTAL_GRID_CHARGE_ENERGY=30
        self.PIN_O_TOTAL_DC_SUM_ENERGY=31
        self.PIN_O_TOTAL_DC1_ENERGY=32
        self.PIN_O_TOTAL_DC2_ENERGY=33
        self.PIN_O_TOTAL_DC3_ENERGY=34
        self.PIN_O_TOTAL_AC_SIDE_GRID=35
        self.PIN_O_TOTAL_DC_POWER=36
        self.FRAMEWORK._run_in_context_thread(self.on_init)

########################################################################################################
#### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
###################################################################################################!!!##

        self.interval = None
        self.DEBUG = self.FRAMEWORK.create_debug_section()

        self.fetchMethods = {
            'f32': self.read_32float_2,
            'u16': self.read_u16_1,
            's16': self.read_s16_1
        }

        self.total_consumption_sbc, self.total_power_from_pv_sbc, self.inverter_state = (-1, ) * 3

        ## All Outputs as a dictionary. The key is the number of the output.
        # options: NM =>
        #   M => Battery options - 0: Don't care, 1: only without battery, 2: only with battery
        #   N => Firmware 1.45, new sum registers: 0: Don't care, 1: don't fetch those regs, 2: fetch those regs
        self.registers = {
            self.PIN_O_BATTERY_SOC: { 'type': 'f32', 'regDec': 210, 'lastVal': 0, 'options': 2, 'calc': None, 'name': 'battery SOC'},
            self.PIN_O_BATTERY_CYCLES: { 'type': 'f32', 'regDec': 194, 'lastVal': 0, 'options': 2, 'calc': None, 'name': 'battery cycles'},
            self.PIN_O_BATTERY_VOLTAGE: { 'type': 'f32', 'regDec': 216, 'lastVal': 0.0, 'options': 2, 'calc': None, 'name': 'battery voltage'},
            self.PIN_O_BATTERY_TEMPERATURE: { 'type': 'f32', 'regDec': 214, 'lastVal': 0.0, 'options': 2, 'calc': None, 'name': 'battery temperature'},
            self.PIN_O_HOME_CONSUMPTION_BATTERY: { 'type': 'f32', 'regDec': 106, 'lastVal': 0, 'options': 2, 'calc': None, 'name': 'home consumption battery'},
            self.PIN_O_BATTERY_READY: { 'type': 'f32', 'regDec': 208, 'lastVal': 0, 'options': 2, 'calc': None, 'name': 'battery ready flag'},
            self.PIN_O_HOME_CONSUMPTION_GRID: { 'type': 'f32', 'regDec': 108, 'lastVal': 0, 'options': 0, 'calc': None, 'name': 'home consumption grid'},
            self.PIN_O_HOME_CONSUMPTION_PV: { 'type': 'f32', 'regDec': 116, 'lastVal': 0, 'options': 0, 'calc': None, 'name': 'home consumption PV'},
            self.PIN_O_TOTAL_POWER_FROM_GRID: { 'type': 'f32', 'regDec': 252, 'lastVal': 0, 'options': 0, 'calc': None, 'name': 'total grid consumption'},
            self.PIN_O_INVERTER_POWER: { 'type': 'f32', 'regDec': 575, 'lastVal': 0, 'options': 0, 'calc': None, 'name': 'inverter power'},
            self.PIN_O_INVERTER_STATE_INT: { 'type': 'u16', 'regDec': 56, 'lastVal': 0, 'options': 0, 'calc': None, 'name': 'inverter state INT'},
            self.PIN_O_POWER_FROM_BATTERY: { 'type': 's16', 'regDec': 582, 'lastVal': 0, 'options': 2, 'calc': None, 'name': 'power from battery'},
            self.PIN_O_TOTAL_YIELD: { 'type': 'f32', 'regDec': 320, 'lastVal': 0.0, 'options': 0, 'calc': lambda x: x / 1000, 'name': 'total yield'},
            self.PIN_O_DAILY_YIELD: { 'type': 'f32', 'regDec': 322, 'lastVal': 0.0, 'options': 0, 'calc': lambda x: x / 1000, 'name': 'daily yield'},
            self.PIN_O_MONTHLY_YIELD: { 'type': 'f32', 'regDec': 326, 'lastVal': 0.0, 'options': 0, 'calc': lambda x: x / 1000, 'name': 'monthly yield'},
            self.PIN_O_YEARLY_YIELD: { 'type': 'f32', 'regDec': 324, 'lastVal': 0.0, 'options': 0, 'calc': lambda x: x / 1000, 'name': 'yearly yield'},
            self.PIN_O_DC1_VOLTAGE: { 'type': 'f32', 'regDec': 266, 'lastVal': 0.0, 'options': 0, 'calc': None, 'name': 'PV DC1 voltage'},
            self.PIN_O_DC1_CURRENT: { 'type': 'f32', 'regDec': 258, 'lastVal': 0.0, 'options': 0, 'calc': None, 'name': 'PV DC1 current'},
            self.PIN_O_DC2_VOLTAGE: { 'type': 'f32', 'regDec': 276, 'lastVal': 0.0, 'options': 0, 'calc': None, 'name': 'PV DC2 voltage'},
            self.PIN_O_DC2_CURRENT: { 'type': 'f32', 'regDec': 268, 'lastVal': 0.0, 'options': 0, 'calc': None, 'name': 'PV DC2 current'},
            self.PIN_O_DC3_VOLTAGE: { 'type': 'f32', 'regDec': 286, 'lastVal': 0.0, 'options': 1, 'calc': None, 'name': 'PV DC3 voltage'},
            self.PIN_O_DC3_CURRENT: { 'type': 'f32', 'regDec': 278, 'lastVal': 0.0, 'options': 1, 'calc': None, 'name': 'PV DC3 current'},
            self.PIN_O_TOTAL_DC_CHARGE_ENERGY: { 'type': 'f32', 'regDec': 1046, 'lastVal': 0, 'options': 22, 'calc': lambda x: x / 1000, 'name': 'total dc charge energy'},
            self.PIN_O_TOTAL_DC_DISCHARGE_ENERGY: { 'type': 'f32', 'regDec': 1048, 'lastVal': 0, 'options': 22, 'calc': lambda x: x / 1000, 'name': 'total dc discharge energy'},
            self.PIN_O_TOTAL_AC_CHARGE_ENERGY: { 'type': 'f32', 'regDec': 1050, 'lastVal': 0, 'options': 22, 'calc': lambda x: x / 1000, 'name': 'total ac charge energy'},
            self.PIN_O_TOTAL_AC_DISCHARGE_ENERGY: { 'type': 'f32', 'regDec': 1052, 'lastVal': 0, 'options': 22, 'calc': lambda x: x / 1000, 'name': 'total ac discharge energy'},
            self.PIN_O_TOTAL_GRID_CHARGE_ENERGY: { 'type': 'f32', 'regDec': 1054, 'lastVal': 0, 'options': 22, 'calc': lambda x: x / 1000, 'name': 'total grid charge energy'},
            self.PIN_O_TOTAL_DC_SUM_ENERGY: { 'type': 'f32', 'regDec': 1056, 'lastVal': 0, 'options': 20, 'calc': lambda x: x / 1000, 'name': 'total DC PV energy'},
            self.PIN_O_TOTAL_DC1_ENERGY: { 'type': 'f32', 'regDec': 1058, 'lastVal': 0, 'options': 20, 'calc': lambda x: x / 1000, 'name': 'total DC1 PV energy'},
            self.PIN_O_TOTAL_DC2_ENERGY: { 'type': 'f32', 'regDec': 1060, 'lastVal': 0, 'options': 20, 'calc': lambda x: x / 1000, 'name': 'total DC2 PV energy'},
            self.PIN_O_TOTAL_DC3_ENERGY: { 'type': 'f32', 'regDec': 1062, 'lastVal': 0, 'options': 21, 'calc': lambda x: x / 1000, 'name': 'total DC3 PV energy'},
            self.PIN_O_TOTAL_AC_SIDE_GRID: { 'type': 'f32', 'regDec': 1064, 'lastVal': 0, 'options': 20, 'calc': lambda x: x / 1000, 'name': 'total AC into grid'},
            self.PIN_O_TOTAL_POWER_FROM_PV: { 'type': 'f32', 'regDec': 1066, 'lastVal': 0, 'options': 20, 'calc': None, 'name': 'total DC power'},
        }

        self.inverter_State_Mapping = ["Off", "Init", "IsoMeas", "Grid Check", "Start Up", "-", "Feed In", "Throttled",
                                       "Ext. Switch Off", "Update", "Standby", "Grid Sync", "Grid Pre-Check",
                                       "Grid Switch Off", "Overheating", "Shutdown", "Improper DC Voltage!", "ESB", "Unknown"]

#############

    def on_interval(self):
        ip_address = str(self._get_input_value(self.PIN_I_INVERTER_IP))
        port = int(self._get_input_value(self.PIN_I_PORT))
        unit_id = int(self._get_input_value(self.PIN_I_UNIT_ID))
        battery = bool(self._get_input_value(self.PIN_I_BATTERY_AT_DC3))
        read_total_regs = bool(self._get_input_value(self.PIN_I_TOTAL_SUM_REGISTERS_EXISTS))

        client = None
        try:
            self.DEBUG.set_value("Connection IP:Port (UnitID)", ip_address + ":" + str(port) + " (" + str(unit_id) + ") ")
            client = ModbusTcpClient(ip_address, port)
            client.connect()

            self.read_power_values(client, unit_id, battery, read_total_regs)
        except Exception as err:
            self.DEBUG.set_value("Last exception msg logged", err.message)
            raise
        finally:
            if client:
                client.close()

    def read_power_values(self, client, unit_id, battery, read_total_regs):

        # fetch all registers
        for outputNum in self.registers:
            if self.must_read_register(outputNum, battery, read_total_regs) is True:
                func = self.fetchMethods.get(self.registers[outputNum]['type']) # Get handler method
                value = func(client, unit_id, self.registers[outputNum]['regDec']) # fetch modbus values
                self.DEBUG.set_value(self.registers[outputNum]['name'], value)  # set Debug raw value

            # apply calculation lambda if set
            if self.registers[outputNum]['calc'] is not None:
                value = self.registers[outputNum]['calc'](value)

            # send by change (sbc) // set value to output if value has changed
            if self.registers[outputNum]['lastVal'] != value:
                self._set_output_value(outputNum, value)  # set value to output PIN
                self.registers[outputNum]['lastVal'] = value  # assign value to variable

        # Calculate current total home consumption
        total_consumption = self.registers[self.PIN_O_HOME_CONSUMPTION_BATTERY]['lastVal'] + \
                            self.registers[self.PIN_O_HOME_CONSUMPTION_GRID]['lastVal'] + \
                            self.registers[self.PIN_O_HOME_CONSUMPTION_PV]['lastVal']

        if self.total_consumption_sbc != total_consumption:
            self.DEBUG.set_value("total consumption calc", total_consumption)
            self._set_output_value(self.PIN_O_HOME_CONSUMPTION_TOTAL, total_consumption)
            self.total_consumption_sbc = total_consumption

        # Calculate total power from PV
        total_power_from_pv = -1 * (min(0, self.registers[self.PIN_O_POWER_FROM_BATTERY]['lastVal']) +
                                    min(0, self.registers[self.PIN_O_TOTAL_POWER_FROM_GRID]['lastVal']) +
                                    self.registers[self.PIN_O_HOME_CONSUMPTION_PV]['lastVal'])

        if self.total_power_from_pv_sbc != total_power_from_pv:
            self.DEBUG.set_value("total power pv calc", total_power_from_pv)
            self._set_output_value(self.PIN_O_TOTAL_POWER_FROM_PV, total_power_from_pv)
            self.total_power_from_pv_sbc = total_power_from_pv

        ## Inverter state integer to string
        inverter_state = self.convert_to_inverter_statusstring(self.registers[self.PIN_O_INVERTER_STATE_INT]['lastVal'])
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
                                                      wordorder=self.word_order()).decode_16bit_uint()
        else:
            return -1

    def read_s16_1(self, client, unit_id, reg_addr):
        result = client.read_holding_registers(reg_addr, 1, unit=unit_id)
        if not result.isError():
            return BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big,
                                                      wordorder=self.word_order()).decode_16bit_int()
        else:
            return -1

    def read_32float_2(self, client, unit_id, reg_addr):
        result = client.read_holding_registers(reg_addr, 2, unit=unit_id)
        if not result.isError():
            return BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big,
                                                      wordorder=self.word_order()).decode_32bit_float()
        else:
            return -1

    def word_order(self):
        if int(self._get_input_value(self.PIN_I_UNIT_ID)) == 1:
            return Endian.Big
        else:
            return Endian.Little

    #############

    def convert_to_inverter_statusstring(self, inverter_status_int):
        if 0 <= inverter_status_int < len(self.inverter_State_Mapping):
            return self.inverter_State_Mapping[inverter_status_int]
        else:
            return "---"

    def must_read_register(self, outputNum, battery, read_total_regs):
        register = self.registers[outputNum]
        reg_option = register['options']

        read_reg = True

        battery_option = reg_option % 10
        if battery is True and battery_option is 1:
            read_reg = False
        elif battery is False and battery_option is 2:
            read_reg = False

        reg_option = reg_option / 10
        if read_total_regs is True and reg_option is 1:
            read_reg = False
        elif read_total_regs is False and reg_option is 2:
            read_reg = False

        return read_reg
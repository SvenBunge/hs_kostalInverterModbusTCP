# coding: UTF-8

import pymodbus  # To not delete this module reference!!
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ConnectionException
from pymodbus.pdu import ExceptionResponse
from pymodbus.register_read_message import ReadHoldingRegistersResponse
import time

##!!!!##################################################################################################
#### Own written code can be placed above this commentblock . Do not change or delete commentblock! ####
########################################################################################################
##** Code created by generator - DO NOT CHANGE! **##

class KostalInverterModbusTCP14180(hsl20_3.BaseModule):

    def __init__(self, homeserver_context):
        hsl20_3.BaseModule.__init__(self, homeserver_context, "kostalInverterModbusTCP14180")
        self.FRAMEWORK = self._get_framework()
        self.LOGGER = self._get_logger(hsl20_3.LOGGING_NONE,())
        self.PIN_I_SWITCH=1
        self.PIN_I_FETCH_INTERVAL=2
        self.PIN_I_INVERTER_IP=3
        self.PIN_I_PORT=4
        self.PIN_I_UNIT_ID=5
        self.PIN_I_ENABLE_DEBUG=6
        self.PIN_O_HOME_CONSUMPTION_BATTERY=1
        self.PIN_O_HOME_CONSUMPTION_GRID=2
        self.PIN_O_HOME_CONSUMPTION_PV=3
        self.PIN_O_HOME_CONSUMPTION_TOTAL=4
        self.PIN_O_TOTAL_POWER_FROM_GRID=5
        self.PIN_O_TOTAL_POWER_FROM_PV=6
        self.PIN_O_MAX_INVERTER_POWER=7
        self.PIN_O_INVERTER_POWER=8
        self.PIN_O_INVERTER_STATE_INT=9
        self.PIN_O_INVERTER_STATE=10
        self.PIN_O_ISOLATION_RESISTANCE=11
        self.PIN_O_COS_PHI=12
        self.PIN_O_GRID_FREQ=13
        self.PIN_O_L1_VOLTAGE=14
        self.PIN_O_L1_CURRENT=15
        self.PIN_O_L1_POWER=16
        self.PIN_O_L2_VOLTAGE=17
        self.PIN_O_L2_CURRENT=18
        self.PIN_O_L2_POWER=19
        self.PIN_O_L3_VOLTAGE=20
        self.PIN_O_L3_CURRENT=21
        self.PIN_O_L3_POWER=22
        self.PIN_O_POWER_FROM_BATTERY=23
        self.PIN_O_TOTAL_YIELD=24
        self.PIN_O_DAILY_YIELD=25
        self.PIN_O_MONTHLY_YIELD=26
        self.PIN_O_YEARLY_YIELD=27
        self.PIN_O_DC1_VOLTAGE=28
        self.PIN_O_DC1_CURRENT=29
        self.PIN_O_DC1_POWER=30
        self.PIN_O_DC2_VOLTAGE=31
        self.PIN_O_DC2_CURRENT=32
        self.PIN_O_DC2_POWER=33
        self.PIN_O_DC3_VOLTAGE=34
        self.PIN_O_DC3_CURRENT=35
        self.PIN_O_DC3_POWER=36
        self.PIN_O_BATTERY_SOC=37
        self.PIN_O_BATTERY_CYCLES=38
        self.PIN_O_BATTERY_WORK_CAPACITY=39
        self.PIN_O_BATTERY_VOLTAGE=40
        self.PIN_O_BATTERY_TEMPERATURE=41
        self.PIN_O_BATTERY_READY=42
        self.PIN_O_TOTAL_DC_CHARGE_ENERGY=43
        self.PIN_O_TOTAL_DC_DISCHARGE_ENERGY=44
        self.PIN_O_TOTAL_AC_CHARGE_ENERGY=45
        self.PIN_O_TOTAL_AC_DISCHARGE_ENERGY=46
        self.PIN_O_TOTAL_GRID_CHARGE_ENERGY=47
        self.PIN_O_TOTAL_DC_SUM_ENERGY=48
        self.PIN_O_TOTAL_DC1_ENERGY=49
        self.PIN_O_TOTAL_DC2_ENERGY=50
        self.PIN_O_TOTAL_DC3_ENERGY=51
        self.PIN_O_TOTAL_AC_SIDE_GRID=52
        self.PIN_O_TOTAL_DC_POWER=53
        self.FRAMEWORK._run_in_context_thread(self.on_init)

########################################################################################################
#### Own written code can be placed after this commentblock . Do not change or delete commentblock! ####
###################################################################################################!!!##

        self.INTERNAL_ENDIAN = 1
        self.INTERNAL_ENERGY_SCALEFACTOR = 2
        self.INTERNAL_POWER_SCALEFACTOR = 3

        self.interval = None
        self.client = None
        self.DEBUG = None
        self.register_copy = [0] * 1068
        self.modbus_read = [{"from": 5, "to": 7},
                            {"from": 56, "to": 58},
                            {"from": 100, "to": 196},
                            {"from": 200, "to": 296},
                            {"from": 320, "to": 327},
                            {"from": 529, "to": 589},
                            {"from": 1046, "to": 1068}]

        self.skip_interval_counter = 0

        self.fetchMethods = {
            'f32': self.read_32float_2,
            'u16': self.read_u16_1,
            'u32': self.read_u32_1,
            'i16': self.read_i16_1,
            'scale16': self.read16float_power_scaled,
            'r32e': self.read32float_energy_scaled,
            'r32p': self.read32float_power_scaled
        }

        self.total_consumption_sbc, self.total_power_from_pv_sbc, self.inverter_state = (-1, ) * 3

        self.internalRegisters = {
            self.INTERNAL_ENDIAN: {'type': 'u16', 'regDec': 5, 'lastVal': 0, 'calc': None, 'name': 'Internal:Endianes'},
            self.INTERNAL_ENERGY_SCALEFACTOR: {'type': 'i16', 'regDec': 579, 'lastVal': 0, 'calc': None, 'name': 'Internal:Energy scalefactor'},
            self.INTERNAL_POWER_SCALEFACTOR: {'type': 'i16', 'regDec': 576, 'lastVal': 0, 'calc': None, 'name': 'Internal:Power scalefactor'}
        }

        # All Outputs as a dictionary. The key is the number of the output.
        self.registers = {
            self.PIN_O_BATTERY_SOC: {'type': 'f32', 'regDec': 210, 'lastVal': 0, 'calc': None, 'name': 'battery SOC'},
            self.PIN_O_BATTERY_CYCLES: {'type': 'f32', 'regDec': 194, 'lastVal': 0, 'calc': None, 'name': 'battery cycles'},
            self.PIN_O_BATTERY_WORK_CAPACITY: {'type': 'u32', 'regDec': 529, 'lastVal': 0.0, 'calc': None, 'name': 'battery work capacity'},
            self.PIN_O_BATTERY_VOLTAGE: {'type': 'f32', 'regDec': 216, 'lastVal': 0.0, 'calc': None, 'name': 'battery voltage'},
            self.PIN_O_BATTERY_TEMPERATURE: {'type': 'f32', 'regDec': 214, 'lastVal': 0.0, 'calc': None, 'name': 'battery temperature'},
            self.PIN_O_HOME_CONSUMPTION_BATTERY: {'type': 'f32', 'regDec': 106, 'lastVal': 0, 'calc': None, 'name': 'home consumption battery'},
            self.PIN_O_BATTERY_READY: {'type': 'f32', 'regDec': 208, 'lastVal': 0, 'calc': None, 'name': 'battery ready flag'},
            self.PIN_O_HOME_CONSUMPTION_GRID: {'type': 'f32', 'regDec': 108, 'lastVal': 0, 'calc': None, 'name': 'home consumption grid'},
            self.PIN_O_HOME_CONSUMPTION_PV: {'type': 'f32', 'regDec': 116, 'lastVal': 0, 'calc': None, 'name': 'home consumption PV'},
            self.PIN_O_TOTAL_POWER_FROM_GRID: {'type': 'f32', 'regDec': 252, 'lastVal': 0, 'calc': None, 'name': 'total grid consumption'},
            self.PIN_O_INVERTER_POWER: {'type': 'scale16', 'regDec': 575, 'lastVal': 0, 'calc': None, 'name': 'inverter power'},
            # difference: Plenticore: u16, PIKO CI: Get 32bit and shift 16bit if value is in wrong register.
            self.PIN_O_INVERTER_STATE_INT: {'type': 'u32', 'regDec': 56, 'lastVal': 0, 'calc': lambda x: x if x < 65535 else x >> 16, 'name': 'inverter state INT'},
            self.PIN_O_ISOLATION_RESISTANCE: {'type': 'f32', 'regDec': 120, 'lastVal': 0, 'calc': lambda x: x / 1000000, 'name': 'Isolation resistance'},
            self.PIN_O_COS_PHI: {'type': 'f32', 'regDec': 150, 'lastVal': 0, 'calc': None, 'name': 'Actual cos phi'},
            self.PIN_O_GRID_FREQ: {'type': 'f32', 'regDec': 152, 'lastVal': 0, 'calc': None, 'name': 'Grid frequency'},
            self.PIN_O_MAX_INVERTER_POWER: {'type': 'u16', 'regDec': 531, 'lastVal': 0, 'calc': None, 'name': 'Max Inverter power / limit'},
            self.PIN_O_L1_VOLTAGE: {'type': 'f32', 'regDec': 158, 'lastVal': 0, 'calc': None, 'name': 'L1 voltage in V'},
            self.PIN_O_L1_CURRENT: {'type': 'f32', 'regDec': 154, 'lastVal': 0, 'calc': None, 'name': 'L1 current in A'},
            self.PIN_O_L1_POWER: {'type': 'f32', 'regDec': 156, 'lastVal': 0, 'calc': None, 'name': 'L1 power in W'},
            self.PIN_O_L2_VOLTAGE: {'type': 'f32', 'regDec': 164, 'lastVal': 0, 'calc': None, 'name': 'L2 voltage in V'},
            self.PIN_O_L2_CURRENT: {'type': 'f32', 'regDec': 160, 'lastVal': 0, 'calc': None, 'name': 'L2 current in A'},
            self.PIN_O_L2_POWER: {'type': 'f32', 'regDec': 162, 'lastVal': 0, 'calc': None, 'name': 'L2 power in W'},
            self.PIN_O_L3_VOLTAGE: {'type': 'f32', 'regDec': 170, 'lastVal': 0, 'calc': None, 'name': 'L3 voltage in V'},
            self.PIN_O_L3_CURRENT: {'type': 'f32', 'regDec': 166, 'lastVal': 0, 'calc': None, 'name': 'L3 current in A'},
            self.PIN_O_L3_POWER: {'type': 'f32', 'regDec': 168, 'lastVal': 0, 'calc': None, 'name': 'L3 power in W'},
            self.PIN_O_POWER_FROM_BATTERY: {'type': 'scale16', 'regDec': 582, 'lastVal': 0, 'calc': None, 'name': 'power from battery'},
            self.PIN_O_TOTAL_YIELD: {'type': 'f32', 'regDec': 320, 'lastVal': 0.0, 'calc': lambda x: x / 1000, 'name': 'total yield'},
            self.PIN_O_DAILY_YIELD: {'type': 'f32', 'regDec': 322, 'lastVal': 0.0, 'calc': lambda x: x / 1000, 'name': 'daily yield'},
            self.PIN_O_MONTHLY_YIELD: {'type': 'f32', 'regDec': 326, 'lastVal': 0.0, 'calc': lambda x: x / 1000, 'name': 'monthly yield'},
            self.PIN_O_YEARLY_YIELD: {'type': 'f32', 'regDec': 324, 'lastVal': 0.0, 'calc': lambda x: x / 1000, 'name': 'yearly yield'},
            self.PIN_O_DC1_VOLTAGE: {'type': 'f32', 'regDec': 266, 'lastVal': 0.0, 'calc': None, 'name': 'PV DC1 voltage'},
            self.PIN_O_DC1_CURRENT: {'type': 'f32', 'regDec': 258, 'lastVal': 0.0, 'calc': None, 'name': 'PV DC1 current'},
            self.PIN_O_DC1_POWER: {'type': 'f32', 'regDec': 260, 'lastVal': 0.0, 'calc': None, 'name': 'PV DC1 power'},
            self.PIN_O_DC2_VOLTAGE: {'type': 'f32', 'regDec': 276, 'lastVal': 0.0, 'calc': None, 'name': 'PV DC2 voltage'},
            self.PIN_O_DC2_CURRENT: {'type': 'f32', 'regDec': 268, 'lastVal': 0.0, 'calc': None, 'name': 'PV DC2 current'},
            self.PIN_O_DC2_POWER: {'type': 'f32', 'regDec': 270, 'lastVal': 0.0, 'calc': None, 'name': 'PV DC2 power'},
            self.PIN_O_DC3_VOLTAGE: {'type': 'f32', 'regDec': 286, 'lastVal': 0.0, 'calc': None, 'name': 'PV DC3 voltage'},
            self.PIN_O_DC3_CURRENT: {'type': 'f32', 'regDec': 278, 'lastVal': 0.0, 'calc': None, 'name': 'PV DC3 current'},
            self.PIN_O_DC3_POWER: {'type': 'f32', 'regDec': 280, 'lastVal': 0.0, 'calc': None, 'name': 'PV DC3 power'},
            self.PIN_O_TOTAL_DC_CHARGE_ENERGY: {'type': 'r32e', 'regDec': 1046, 'lastVal': 0, 'calc': lambda x: x / 1000, 'name': 'total dc charge energy'},
            self.PIN_O_TOTAL_DC_DISCHARGE_ENERGY: {'type': 'r32e', 'regDec': 1048, 'lastVal': 0, 'calc': lambda x: x / 1000, 'name': 'total dc discharge energy'},
            self.PIN_O_TOTAL_AC_CHARGE_ENERGY: {'type': 'r32e', 'regDec': 1050, 'lastVal': 0, 'calc': lambda x: x / 1000, 'name': 'total ac charge energy'},
            self.PIN_O_TOTAL_AC_DISCHARGE_ENERGY: {'type': 'r32e', 'regDec': 1052, 'lastVal': 0, 'calc': lambda x: x / 1000, 'name': 'total ac discharge energy'},
            self.PIN_O_TOTAL_GRID_CHARGE_ENERGY: {'type': 'r32e', 'regDec': 1054, 'lastVal': 0, 'calc': lambda x: x / 1000, 'name': 'total grid charge energy'},
            self.PIN_O_TOTAL_DC_SUM_ENERGY: {'type': 'r32e', 'regDec': 1056, 'lastVal': 0, 'calc': lambda x: x / 1000, 'name': 'total DC PV energy'},
            self.PIN_O_TOTAL_DC1_ENERGY: {'type': 'r32e', 'regDec': 1058, 'lastVal': 0, 'calc': lambda x: x / 1000, 'name': 'total DC1 PV energy'},
            self.PIN_O_TOTAL_DC2_ENERGY: {'type': 'r32e', 'regDec': 1060, 'lastVal': 0, 'calc': lambda x: x / 1000, 'name': 'total DC2 PV energy'},
            self.PIN_O_TOTAL_DC3_ENERGY: {'type': 'r32e', 'regDec': 1062, 'lastVal': 0, 'calc': lambda x: x / 1000, 'name': 'total DC3 PV energy'},
            self.PIN_O_TOTAL_AC_SIDE_GRID: {'type': 'r32e', 'regDec': 1064, 'lastVal': 0, 'calc': lambda x: x / 1000, 'name': 'total AC into grid'},
            self.PIN_O_TOTAL_DC_POWER: {'type': 'r32p', 'regDec': 1066, 'lastVal': 0, 'calc': None, 'name': 'total DC power'},
        }

        self.inverter_State_Mapping = ["Off", "Init", "IsoMeas", "Grid Check", "Start Up", "-", "Feed In", "Throttled",
                                       "Ext. Switch Off", "Update", "Standby", "Grid Sync", "Grid Pre-Check",
                                       "Grid Switch Off", "Overheating", "Shutdown", "Improper DC Voltage", "ESB", "Unknown"]

#############

    def on_interval(self):
        self.log_debug("Due error skipping N intervals: ", self.skip_interval_counter)
        
        if self.skip_interval_counter > 0:
            self.skip_interval_counter -= 1
            return

        ip_address = str(self._get_input_value(self.PIN_I_INVERTER_IP))
        port = int(self._get_input_value(self.PIN_I_PORT))
        unit_id = int(self._get_input_value(self.PIN_I_UNIT_ID))

        try:
            self.log_debug("Connection IP:Port (UnitID)", ip_address + ":" + str(port) + " (" + str(unit_id) + ") ")
            if self.client is None:
                self.client = ModbusTcpClient(ip_address, port)
            if self.client.is_socket_open() is False:
                self.client.connect()

            # fetch all values at once
            for read_task in self.modbus_read:
                length = read_task["to"] - read_task["from"]
                result = self.client.read_holding_registers(read_task["from"], length, unit=unit_id)
                self.log_debug("result", result)
                if isinstance(result, ReadHoldingRegistersResponse):
                    self.register_copy = self.register_copy[:read_task["from"]] + result.registers + \
                                         self.register_copy[read_task["to"]:]

            self.extract_power_values(self.register_copy)
        except ConnectionException as con_err:
            # Error during comm. Maybe temp. network error. try again in 5 Minutes (when used with 5 seconds interval)
            self.skip_interval_counter = 60
            self.log_debug("Last exception msg logged", "retrying after 60 intervals: " + con_err.message)
        except Exception as err:
            # Let's try it again in 30 Minutes (when used with 5 seconds interval)
            self.skip_interval_counter = 360
            self.log_debug("Last exception msg logged", "retrying after 360 intervals: " + err.message)

    def extract_power_values(self, register_res):

        # extract configuration registers
        for internalNum in self.internalRegisters:
            func = self.fetchMethods.get(self.internalRegisters[internalNum]['type'])  # Get handler method
            value = func(register_res, self.internalRegisters[internalNum]['regDec'])  # fetch modbus values
            self.log_debug(self.internalRegisters[internalNum]['name'], value)  # set Debug raw value
            self.internalRegisters[internalNum]['lastVal'] = value  # assign value to variable

        # extract all registers
        for outputNum in self.registers:
            func = self.fetchMethods.get(self.registers[outputNum]['type'])  # Get handler method
            value = func(register_res, self.registers[outputNum]['regDec'])  # fetch modbus values
            self.log_debug(self.registers[outputNum]['name'], value)  # set Debug raw value

            # apply calculation lambda if set
            if self.registers[outputNum]['calc']:
                value = self.registers[outputNum]['calc'](value)

            # send by change (sbc) // set value to output if value has changed
            if self.registers[outputNum]['lastVal'] != value:
                self._set_output_value(outputNum, value)  # set value to output PIN
                self.registers[outputNum]['lastVal'] = value  # assign value to variable

        self.calculate_other_outputs()

    def calculate_other_outputs(self):
        # Calculate current total home consumption
        total_consumption = self.registers[self.PIN_O_HOME_CONSUMPTION_BATTERY]['lastVal'] + \
                            self.registers[self.PIN_O_HOME_CONSUMPTION_GRID]['lastVal'] + \
                            self.registers[self.PIN_O_HOME_CONSUMPTION_PV]['lastVal']
        if self.total_consumption_sbc != total_consumption:
            self.log_debug("total consumption calc", total_consumption)
            self._set_output_value(self.PIN_O_HOME_CONSUMPTION_TOTAL, total_consumption)
            self.total_consumption_sbc = total_consumption
        # Calculate total power from PV
        total_power_from_pv = -1 * (min(0, self.registers[self.PIN_O_POWER_FROM_BATTERY]['lastVal']) +
                                    min(0, self.registers[self.PIN_O_TOTAL_POWER_FROM_GRID]['lastVal'])) + \
                              self.registers[self.PIN_O_HOME_CONSUMPTION_PV]['lastVal']
        if self.total_power_from_pv_sbc != total_power_from_pv:
            self.log_debug("total power pv calc", total_power_from_pv)
            self._set_output_value(self.PIN_O_TOTAL_POWER_FROM_PV, total_power_from_pv)
            self.total_power_from_pv_sbc = total_power_from_pv
        # Inverter state integer to string
        inverter_state = self.convert_to_inverter_status_string(
            self.registers[self.PIN_O_INVERTER_STATE_INT]['lastVal'])
        if self.inverter_state != inverter_state:
            self._set_output_value(self.PIN_O_INVERTER_STATE, inverter_state)
            self.inverter_state = inverter_state

    #############

    def on_init(self):
        self.interval = self.FRAMEWORK.create_interval()
        if bool(self._get_input_value(self.PIN_I_SWITCH)):
            self.interval.set_interval(self._get_input_value(self.PIN_I_FETCH_INTERVAL) * 1000, self.on_interval)
            self.interval.start()

    def on_input_value(self, index, value):
        if index == self.PIN_I_SWITCH or index == self.PIN_I_FETCH_INTERVAL:
            self.interval.stop()
            self.interval.set_interval(self._get_input_value(self.PIN_I_FETCH_INTERVAL) * 1000, self.on_interval)
            if bool(self._get_input_value(self.PIN_I_SWITCH)):
                self.interval.start()
        elif index == self.PIN_I_INVERTER_IP or index == self.PIN_I_PORT:
            self.client = None  # Next iteration client is rebuild with actual ip and port.

    def read_u16_1(self, registers, addr):
        return BinaryPayloadDecoder.fromRegisters(self.res_extract(registers, addr, 1), byteorder=Endian.Big,
                                                  wordorder=self.word_order()).decode_16bit_uint()

    def read_u32_1(self, registers, addr):
        return BinaryPayloadDecoder.fromRegisters(self.res_extract(registers, addr, 2), byteorder=Endian.Big,
                                                  wordorder=self.word_order()).decode_32bit_uint()

    def read_i16_1(self, registers, addr):
        return BinaryPayloadDecoder.fromRegisters(self.res_extract(registers, addr, 1), byteorder=Endian.Big,
                                                  wordorder=self.word_order()).decode_16bit_int()

    def read_32float_2(self, registers, addr):
        return BinaryPayloadDecoder.fromRegisters(self.res_extract(registers, addr, 2), byteorder=Endian.Big,
                                                  wordorder=self.word_order()).decode_32bit_float()

    def read16float_power_scaled(self, registers, addr):
        result = self.read_i16_1(registers, addr)
        return result * 10 ** self.internalRegisters[self.INTERNAL_POWER_SCALEFACTOR]['lastVal']

    def read32float_energy_scaled(self, registers, addr):
        result = self.read_32float_2(registers, addr)
        return result * 10 ** self.internalRegisters[self.INTERNAL_ENERGY_SCALEFACTOR]['lastVal']

    def read32float_power_scaled(self, registers, addr):
        result = self.read_32float_2(registers, addr)
        return result * 10 ** self.internalRegisters[self.INTERNAL_POWER_SCALEFACTOR]['lastVal']

    def word_order(self):
        if bool(self.internalRegisters[self.INTERNAL_ENDIAN]['lastVal']):
            return Endian.Big

        return Endian.Little

    def res_extract(self, result_res, start, length):
        end = start + length
        return result_res[start:end]

    #############

    def convert_to_inverter_status_string(self, inverter_status_int):
        if 0 <= inverter_status_int < len(self.inverter_State_Mapping):
            return self.inverter_State_Mapping[inverter_status_int]

        return "---"

    def log_debug(self, key, value):
        if bool(self._get_input_value(self.PIN_I_ENABLE_DEBUG)):
            if not self.DEBUG:
                self.DEBUG = self.FRAMEWORK.create_debug_section()

            self.DEBUG.set_value(str(key), str(value))

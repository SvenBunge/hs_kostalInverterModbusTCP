# coding: UTF-8
import logging
import pymodbus
from pymodbus.constants import Endian, Defaults
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

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


    def read_current_power_values(self, ip_address, port_number, unit_id):
 #       client = None
 #       try:
            self.DEBUG.set_value("creating client with Defaults:", Defaults.Timeout)
            self.DEBUG.set_value("creating client with IP:", ip_address)
            self.DEBUG.set_value("creating client with Port:", port_number)
            self.DEBUG.set_value("creating client with UnitID:", unit_id)
            client = ModbusClient('192.168.80.20', port=1502)
            client.connect()
            self.DEBUG.set_value("client connection established", "yes")
            ###
            ## read power values
            ###
            self.read_power_values(client, unit_id)
#        except Exception as e:
#            print(e)
#        finally:
#            if client:
#                client.close()

    def read_power_values(self, client, unit_id):
        # Battery SOC (% - unsigned 16bit int)
        home_battery_soc = self.read_u16_1(client, unit_id, 514)
        self.DEBUG.set_value('batterySOC', home_battery_soc)
        self._set_output_value(self.PIN_O_BATTERY_SOC, home_battery_soc)

        # # Home own consumption from battery (W - 32bit float)
        home_consumption_battery = self.read_32float_2(client, unit_id, 106)
        self.DEBUG.set_value('batteryCONSUMPTION', home_consumption_battery)
        self._set_output_value(self.PIN_O_HOME_CONSUMPTION_BATTERY, home_consumption_battery)
        #
        # # Home own consumption from grid (W - 32bit float)
        home_consumption_grid = self.read_32float_2(client, unit_id, 108)
        self.DEBUG.set_value('gridCONSUMPTION', home_consumption_grid)
        self._set_output_value(self.PIN_O_HOME_CONSUMPTION_GRID, home_consumption_grid)
        #
        # # Home own consumption from PV (W - 32bit float)
        home_consumption_pv = self.read_32float_2(client, unit_id, 116)
        self.DEBUG.set_value('pvCONSUMPTION', home_consumption_pv)
        self._set_output_value(self.PIN_O_HOME_CONSUMPTION_PV, home_consumption_pv)
        #
        # # Calculate current total home consumption
        home_consumption = home_consumption_battery + home_consumption_grid + home_consumption_pv
        self.DEBUG.set_value('totalCONSUMPTION', home_consumption)
        self._set_output_value(self.PIN_O_HOME_CONSUMPTION_TOTAL, home_consumption)
        #
        total_power = self.read_32float_2(client, unit_id, 252)
        self.DEBUG.set_value('totalPOWER', total_power)
        self._set_output_value(self.PIN_O_TOTAL_POWER_FROM_GRID, total_power)
        #
        inverter_power = self.read_32float_2(client, unit_id, 575)
        self.DEBUG.set_value('inverterPOWER', inverter_power)
        self._set_output_value(self.PIN_O_INVERTER_POWER, inverter_power)
        #
        battery_power = self.read_s16_1(client, unit_id, 582)
        self.DEBUG.set_value('batteryPOWER', battery_power)
        self._set_output_value(self.PIN_O_POWER_FROM_BATTERY, battery_power)
        #
        total_power_from_pv = battery_power + total_power + home_consumption_pv
        self.DEBUG.set_value('pvPOWER', total_power_from_pv)
        self._set_output_value(self.PIN_O_TOTAL_POWER_FROM_PV, total_power_from_pv)

    def read_u16_1(self, client, unit_id, reg_addr):
        result = client.read_holding_registers(reg_addr, 1, unit=unit_id)
        if not result.isError():
            return BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big,
                                                  wordorder=Endian.Little).decode_16bit_uint()
        else:
            return -1

    def read_s16_1(self, client, unit_id, reg_addr):
        result = client.read_holding_registers(reg_addr, 1, unit=unit_id)
        if not result.isError():
            return BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big,
                                                  wordorder=Endian.Little).decode_16bit_int()
        else:
            return -1

    def read_32float_2(self, client, unit_id, reg_addr):
        result = client.read_holding_registers(reg_addr, 2, unit=unit_id)
        if not result.isError():
            return BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big,
                                                  wordorder=Endian.Little).decode_32bit_float()
        else:
            return -1

    def on_init(self):
        self.DEBUG = self.FRAMEWORK.create_debug_section()

    def on_input_value(self, index, value):
        if index == self.PIN_I_TRIGGER:
            ip_address = str(self._get_input_value(self.PIN_I_INVERTER_IP))
            port = int(self._get_input_value(self.PIN_I_PORT))
            unit_id = int(self._get_input_value(self.PIN_I_UNIT_ID))
            self.DEBUG.set_value("IP:", ip_address)
            self.read_current_power_values(ip_address, port, unit_id)

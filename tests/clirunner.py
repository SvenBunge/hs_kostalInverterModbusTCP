
import schedule
import time
KostalInverterReader = __import__('10001_kostalmodbus')

class DummyHomeServer:

    def __init__(self):
        self.PIN_I_TRIGGER = 1
        self.PIN_I_TIME_CURRENT_POWER_VALUES = 2
        self.PIN_I_INVERTER_IP = 3
        self.PIN_I_PORT = 4
        self.PIN_I_UNIT_ID = 5
        self.PIN_O_BATTERY_SOC = 1
        self.PIN_O_HOME_CONSUMPTION_BATTERY = 2
        self.PIN_O_HOME_CONSUMPTION_GRID = 3
        self.PIN_O_HOME_CONSUMPTION_PV = 4
        self.PIN_O_HOME_CONSUMPTION_TOTAL = 5
        self.PIN_O_TOTAL_POWER_FROM_GRID = 6
        self.PIN_O_TOTAL_POWER_FROM_PV = 7
        self.PIN_O_INVERTER_POWER = 8
        self.PIN_O_POWER_FROM_BATTERY = 9

    def set_output_value(self, index, value):
        print(str(index) + ": " + str(value))

    @staticmethod
    def namestr(obj, namespace):
        return [name for name in namespace if namespace[name] is obj]


dummyHomeServer = DummyHomeServer()

kostal_inverter_reader = KostalInverterReader(dummyHomeServer,
                                                "192.168.80.20",
                                                1502,
                                                71)

schedule.every(3).seconds\
    .do(kostal_inverter_reader.read_current_power_values)

while True:
    schedule.run_pending()
    time.sleep(1)


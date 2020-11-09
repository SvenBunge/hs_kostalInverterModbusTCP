# hs_modbus_tcp
Gira Homeserver Logikmodule to poll power values from Kostal solar energy inverter via Modbus TCP.

## Developer Notes

Developed for HomeServer 4.10. Licensed under the LGPL to keep all copies & forks free as well!

:exclamation: **If you fork this project and distribute the module by your own CHANGE the Logikbaustein-ID because 14180 is only for this one and registered to @SvenBunge !!** :exclamation:

If something is wired, wrong or you need something: Just open an issue. Even better: Fix the issue by yourself and fill a pull request as well.

## Installation

Download a [release](https://github.com/SvenBunge/hs_modbus_tcp/releases) and install the module / Logikbaustein like others in Experte.
You find the module in the category "Energiemanagement". Just pic the IP address, port and unit-id of your inverter and wire the output to your communication objects. 

## Documentation

This module fetches power information and states from home solar power inverters of the manufactorer "Kostal". It has been testet with the *Kostal Plenticore Plus 10* with 2 Strings and an BYD battery attached. 

### Holding registers

| Register ID | DPT | Output | Description |
| ----------- | -----| ------ | ----------- |
| 106 | 9.xxx | Own consumption from battery in W (sbc) | The power your home / building is 'eating' from your battery in Watt |
| 108 | 9.xxx | Own consumption from grid in W (sbc) | The power your home / building is fetching from the grid in Watt |
| 116 | 9.xxx | Own consumption from PV in W (sbc) | The power your home / building is powered by your Solar panels |
| xxx | 9.xxx | Total current own consumption in W (sbc) | The power your home / building is using (Grid + Battery + PV) |
| 252 | 9.xxx | Total power from grid (neg: feed-in) (sbc) | The total power the inverter is fetching or feeding from/to the grid. Neg. is feeding. |
| xxx | 9.xxx | Total power from PV generator (sbc) | The total power your inverter fetches from your PV. This value could be limited by the grid feed-in limit (fe. 70%). This value is calculated of battery-charge, home consumption and feed-in power.|
| 575 | 9.xxx | Power of inverter (AC/DC conversion) in W (sbc) | The power that is actually converted between AC and DC |
| 582 | 9.xxx | Power from battery in W (neg: loading) (sbc) | The unload or load (neg.) of the battery in Watt |
| 320 | 9.xxx | Total yield in kWh (sbc) | Total energy ever fetched over the inverter* - in kWh |
| 322 | 9.xxx | Daily yield in kWh (sbc) | Energy fetched over the inverter today* - in kWh |
| 326 | 9.xxx | Monthly yield in kWh (sbc) | Energy fetched over the inverter this month* - in kWh |
| 324 | 9.xxx | Yearly yield in kWh (sbc) | Energy fetched over the inverter this year* - in kWh |
| 266 | 9.xxx | DC1 Voltage in V (sbc) | Actual Voltage of the 1. MPP String |
| 258 | 9.xxx | DC1 Current in A (sbc) | Actual Current of the 1. MPP String |
| 276 | 9.xxx | DC1 Voltage in V (sbc) | Actual Voltage of the 2. MPP String |
| 268 | 9.xxx | DC1 Current in A (sbc) | Actual Current of the 2. MPP String |
| 276 | 9.xxx | DC1 Voltage in V (sbc) | Actual Voltage of the 3. MPP String - zero if a battery is connected! |
| 268 | 9.xxx | DC1 Current in A (sbc) | Actual Current of the 3. MPP String - zero if a battery is connected! |
| 514 | 6.010 | Battery SOC in % (sbc) | Contains the level of the battery in % |
| 194 | 7.001 | Battery Cycles (sbc) | Full cycles of battery unloading/loading (if connected) |
| 216 | 9.xxx | Battery Voltage in V (sbc) | Actual Voltage of the Battery (if connected) |
| 214 | 9.xxx | Battery Temperature in °C (sbc) | Actual Temperature of the Battery (if connected) |

#### Removed because not working

| 529 | 9.xxx | Battery Capacity in kWh (sbc) | Capacity of the Battery (if connected) |

All outputs are only triggered by a change (sbc).
*) Yield: If the battery is loaded DC/DC, the amount of energy is not included in this value. Work around: Add the SOC / 100 * battery capacity to get it approximated.

## Build from scratch

1. Download [Schnittstelleninformation](http://www.hs-help.net/hshelp/gira/other_documentation/Schnittstelleninformationen.zip) from GIRA Homepage
2. Decompress zip, use `HSL SDK/2-0/framework` Folder for development.
3. Checkout this repo to the `projects/modbus_tcp` folder
4. Run the generator.pyc (`python2 ./generator.pyc modbus_tcp`)
5. Import the module `release/1nnnn_kostalmodbus.hsl` into the Experte Software
6. Use the module in your logic editor
 
## Libraries

* pymodbus 1.5.2 - https://github.com/riptideio/pymodbus 
* six (in pymodbus folder) 1.15.0 - https://github.com/benjaminp/six

The shipped libraries may distributed under a different license conditions. Respect those licenses as well!

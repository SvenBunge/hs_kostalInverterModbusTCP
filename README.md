# Kostal-Wechselrichter ModbusTCP (14180)
Gira Homeserver Logikmodule to poll power values from Kostal solar energy inverter via Modbus TCP.

## Developer Notes

Developed for the GIRA HomeServer 4.10 / 4.11!
Licensed under the LGPL to keep all copies & forks free!

:exclamation: **If you fork this project and distribute the module by your own CHANGE the Logikbaustein-ID because 14180 is only for this one and registered to @SvenBunge !!** :exclamation:

If something is wired, wrong or you need something: Just open an issue. Even better: Fix the issue by yourself and fill a pull request.

## Installation

Download a [release](https://github.com/SvenBunge/hs_modbus_tcp/releases) and install the module / Logikbaustein like others in Experte.
You find the module in the category "Energiemanagement". Just pic the IP address, port and unit-id of your inverter and wire the output to your communication objects. 

## Documentation

This module fetches power information and states from home solar power inverters of the manufactorer "Kostal". It has been testet with the *Kostal Plenticore Plus 10* with 2 Strings and an BYD battery attached. 

More [detailed documentation](doc/log14180.md)

#### Removed because not working

| 529 | 9.xxx | Battery Capacity in kWh (sbc) | Capacity of the Battery (if connected) |

All outputs are only triggered by a change (sbc).
*) Yield: If the battery is loaded DC/DC, the amount of energy is not included in this value. Work around: Add the SOC / 100 * battery capacity to get it approximated.

## Build from scratch

1. Download [Schnittstelleninformation](http://www.hs-help.net/hshelp/gira/other_documentation/Schnittstelleninformationen.zip) from GIRA Homepage
2. Decompress zip, use `HSL SDK/2-0/framework` Folder for development.
3. Checkout this repo to the `projects/hs_kostalInverterModbusTCP` folder
4. Run the generator.pyc (`python2 ./generator.pyc hs_kostalInverterModbusTCP`)
5. Import the module `release/14180_kostalInverterModbusTCP.hsl` into the Experte Software
6. Use the module in your logic editor
 
## Libraries

* pymodbus 1.5.2 - https://github.com/riptideio/pymodbus 
* six (in pymodbus folder) 1.15.0 - https://github.com/benjaminp/six

The shipped libraries may distributed under a different license conditions. Respect those licenses as well!

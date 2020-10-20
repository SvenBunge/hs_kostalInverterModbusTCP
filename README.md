# hs_modbus_tcp
Gira Homeserver Logikmodule to poll kostal inverter

Developed for HomeServer 4.10. 

## Installation

1. Download [Schnittstelleninformation](http://www.hs-help.net/hshelp/gira/other_documentation/Schnittstelleninformationen.zip) from GIRA Homepage
2. Decompress zip, use `HSL SDK/2-0/framework` Folder for development.
3. Checkout this repo to the `projects/modbus_tcp` folder
4. Run the generator.pyc (`python2 ./generator.pyc modbus_tcp`)
5. Import the module `release/1nnnn_kostalmodbus.hsl` into the Experte Software
6. Use the module in your logic editor
 
## Libraries

* pymodbus 1.5.2 - https://github.com/riptideio/pymodbus 
* six (in pymodbus folder) 1.15.0 - https://github.com/benjaminp/six


About:

energy_logger.py is a simple application to collect realtime statistics from a Sharp JH-1600E grid connect PV inverter and log the results to pvoutput.org

energy_logger.py makes use of a modified version of Luc Jean's excellent Modbus Toolkit to implement the Modbus protocol used by the inverter.
modbus-tk has been modified to support RS-485 communications by ensuring that RTS is made active during transmit and innavtive during receive.
The modifications I have made are probably not robust however they work for me

The definition of the contents of the inverter's registers have been reverse engineered through comparison with the windows inverter monitoring application provided by Sharp and direct oberservation.


Installation:

Install the following pre-requisites if not already installed:-

- Python 2.6
- Python setup tools http://pypi.python.org/pypi/setuptools
- pyserial http://pypi.python.org/pypi/pyserial

Build and install the modified modbus toolkit supplied with this project as follows:-

cd modbus_tk
sudo python setup.py install

Edit elogger_config.py to set installation specific configuration data, this includes:-

- The device name associated with the RS-485 port connectet to your inverter
- Your pvoutput.org system ID and API key
- Whether or not to enable verbose logging to the console

Hardware installation:

Please see http://power.vacated.net/jh1600e.php for a an excellent desription of how to wire up the inverter.

I am using the following USB-RS485 converter from ebay:-

http://cgi.ebay.com.au/USB-2-0-RS485-RS-485-DB9-Serial-Adapter-Converter-/170485585253?pt=LH_DefaultDomain_0&hash=item27b1bb9565#ht_2998wt_965







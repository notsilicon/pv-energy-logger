"""
 elogger_config.py: Sharp JH-1600E grid connect solar inverter data logger configuration

 (C)2010 - Mike Cornelius - dr@drelectro.com

 This file is distributed under GNU GPL license, see license.txt
 
 Modify this file to suit your installation
"""

RS485_PORT = ''
PVOUTPUT_APIKEY = ''
PVOUTPUT_SYSTEMID = ''

"""
 Select 'console' to enable verbose logging to the console or 'dummy' to disable logging to the console
 By default verbose logging is selected to allow you to test your installation.
 With this enabled you should see the inverter communications stats and stats printed on the console every 10 seconds 
"""

LOGGER = 'console'
#LOGGER = 'dummy'

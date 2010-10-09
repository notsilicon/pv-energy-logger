#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""
 energy_logger: Sharp JH-1600E grid connect solar inverter data logger

 (C)2010 - Mike Cornelius - dr@drelectro.com

 This file is distributed under GNU GPL license, see license.txt
"""

import sys
import time
import serial
import subprocess
import syslog
import logging
from time import localtime, strftime

import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu

from elogger_config import *
from jh1600e import *

logger = modbus_tk.utils.create_logger(LOGGER)  

class logger_runtime:
    def __init__(self):
        self.p_accm = 0
        self.p_count = 0
        self.p_max = 0
        self.p_max_time = localtime()
        self.status_sent = False
        self.output_sent = False



def poll_jh1600e_stats(mb):
    
    stats = jh1600e_stats()
    #Poll dynamic stats multiple times to get both AC and DC stats
    while stats.read_groups != 3:
        res = master.execute(5, cst.READ_INPUT_REGISTERS, 1031, 73)
        logger.info(res)
        stats.parse_dynamic(res)
    return stats
    
def gather_stats(mb,  runtime):
    
    now = localtime()   
    stats = poll_jh1600e_stats(master)
    logger.info(stats)
    if stats.read_groups != 3:
        return
            
    p_inst = float(stats.AC_power)
    runtime.p_accm = runtime.p_accm + p_inst
    runtime.p_count = runtime.p_count + 1
    if p_inst > runtime.p_max:
        runtime.p_max = p_inst
        runtime.p_max_time = now
                
    # every 10 minutes
    if (now.tm_min % 10 == 0) & (stats.status == 'On') & (int(stats.offline_count)<1000):
        if runtime.status_sent == False:
            t_date = 'd={0}'.format(strftime('%Y%m%d'))
            t_time = 't={0}'.format(strftime('%H:%M'))
            t_energy = 'v1={0}'.format(stats.today_Wh)
            #t_power = 'v2={0}'.format(runtime.p_accm/runtime.p_count)
            t_power = 'v2={0}'.format(p_inst)
            cmd = ['/usr/bin/curl',
                '-d', t_date,
                '-d', t_time,
                '-d', t_energy,
                '-d', t_power, 
                '-H', 'X-Pvoutput-Apikey: ' + PVOUTPUT_APIKEY, 
                '-H', 'X-Pvoutput-SystemId: ' + PVOUTPUT_SYSTEMID, 
                'http://pvoutput.org/service/r1/addstatus.jsp']
            #logger.info(cmd)
            l = 'NOW: p_inst = {0}W, p_avg = {1:.1f}W, e_total = {2}Wh, p_max {3}'.format(p_inst,  runtime.p_accm/runtime.p_count, stats.today_Wh, runtime.p_max)
            syslog.syslog(syslog.LOG_INFO,  l)
            ret = subprocess.call (cmd)  
            runtime.p_accm = 0
            runtime.p_count = 0
            runtime.status_sent = True
    else:
        runtime.status_sent = False
                
    if (int(stats.offline_count) > 1000) & (stats.status == 'Off'):
        if runtime.output_sent == False:
            if runtime.p_max != 0:
                data = 'data={0},{1},{2},{3},{4}'.format(strftime('%Y%m%d'), 
                    stats.today_Wh, stats.today_Wh,
                    runtime.p_max, strftime('%H:%M',  runtime.p_max_time))
                cmd = ['/usr/bin/curl',
                    '-d', data, 
                    '-H','X-Pvoutput-Apikey: aa230ec0c4eff06ae22a1563afdf60f103c39046', 
                    '-H','X-Pvoutput-SystemId: 297', 
                    'http://pvoutput.org/service/r1/addoutput.jsp']
                #logger.info(cmd)
                ret = subprocess.call (cmd)
                l = 'EOD: e_total = {0}Wh, p_max = {1}W @ {2}'.format(stats.today_Wh,  runtime.p_max, strftime('%H:%M',  runtime.p_max_time))
                syslog.syslog(syslog.LOG_INFO,  l)
            runtime.output_sent = True
            
    if stats.status == 'On':
        runtime.output_sent = False
                    

    
if __name__ == "__main__":
    
    if RS485_PORT == '':
        print 'RS-485 port not configured\nYou can set this by editing elogger_config.py'
        exit()
        
    runtime = logger_runtime()
    syslog.openlog('energy_logger', 0, syslog.LOG_USER)
    syslog.syslog(syslog.LOG_NOTICE,  'Started')
    
    while True:
        try:
            # Connect to the slave
            master = modbus_rtu.RtuMaster(serial.Serial(port=RS485_PORT, baudrate=9600, bytesize=8, parity='N', stopbits=1, xonxoff=0))
            master.set_timeout(5.0)
            master.set_verbose(True)
            logger.info("connected")
            
            runtime.p_accm = 0
            runtime.p_count = 0
            
            while True:
                now = localtime()
                # Every 10 Seconds
                if now.tm_sec % 10 == 0:
                    gather_stats(master, runtime)
           
                time.sleep(0.5)
                    
                   
            # Get historical data
            #res = master.execute(5, cst.READ_INPUT_REGISTERS, 2047, 28)
            #logger.info(res)
            #stats.parse_history(res)
            
            #logger.info(master.execute(5, cst.READ_COILS, 24611, 1))
            #logger.info(master.execute(5, cst.READ_COILS, 24616, 1))
        

        except modbus_tk.modbus.ModbusError as e:
            logger.error("%s- Code=%d" % (e, e.get_exception_code()))
        except modbus_tk.modbus.ModbusInvalidResponseError :
            pass
            
    syslog.closelog()
    syslog.syslog(syslog.LOG_NOTICE,  'Exiting')

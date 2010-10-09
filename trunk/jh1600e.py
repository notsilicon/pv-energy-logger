"""
 jh1600e: Sharp JH-1600E grid connect solar inverter parser

 (C)2010 - Mike Cornelius - dr@drelectro.com

 This file is distributed under the GNU GPL license, see license.txt
"""


"""

Here's some sample data which may be useful for working out which field is which:-

      0  1  2  3  4  5  6  7   8     9  10    11 12    13 14 15  16 17     18 19 20 21 22 23  24    25   26   27    28 29    30    31 32    33 34 35    36   37    38    39 40   41 42   43 44     45 46     47  48  49  50  51  52  53 54 55 56     57     58     59     60     61     62     63     64     65     66 67 68 69 70 71 72
DC  = 5, 0, 0, 0, 0, 0, 0, 0, 73, 2562, 91, 2310, 3, 2310, 0, 0, 10, 0, 22017, 0, 0, 0, 0, 0, 48, 1872, 206, 390,    0, 0,    0,    0, 3, 2093, 0, 0, 1695, 390, 2558, 8343, 0,    0, 0,   0, 0,     0, 0,     0, 25, 26, 24, 35, 33, 0, 0, 0,  0, 17920, 17686, 17920, 17686, 17921, 17920, 17921, 65535, 65535, 65535, 0, 0, 0, 0, 0, 0
AC  = 5, 0, 0, 0, 0, 0, 0, 0, 73, 2562, 91, 2310, 3, 2310, 0, 0, 10, 0, 22017, 0, 0, 0, 0, 0,  2, 2495, 154, 352, 5004, 0, 2484, 5003, 2, 2090, 0, 0,  840, 110,  355,  765, 0,  473, 0, 137, 2, 36131, 0, 21603, 25, 26, 24, 35, 33, 0, 0, 0, 10, 65535, 65535, 65535, 65535, 65535, 65535,   255,   255,   255,   255, 0, 0, 0, 0, 0, 0

Off = 5, 0, 0, 0, 0, 0, 0, 0, 73, 2562,  0,    0, 0,    0, 0, 0,  0, 0, 22017, 0, 0, 0, 0, 0, 48,    0,   0,   0,    0, 0,    0,    0, 0,    0, 0, 0,    0,   0,    0,    0, 0,    0, 0,   0, 0,     0, 0,     0,  0,  0,  0,  0,  0, 0, 0, 0,  0, 17920, 17686, 17920, 17686, 17921, 17920, 17921, 65535, 65535, 65535, 0, 0, 0, 0, 0, 7934
      5, 0, 0, 0, 0, 0, 0, 0, 73, 2562,  0,    0, 0,    0, 0, 0,  0, 0, 22017, 0, 0, 0, 0, 0,  2,    0,   0,   0,    0, 0,    0,    0, 0,    0, 0, 0,    0,   0,    0,    0, 0, 2478, 0, 673, 3,   773, 0, 25645,  0,  0,  0,  0,  0, 0, 0, 0, 10, 65535, 65535, 65535, 65535, 65535, 65535,   255,   255,   255,   255, 0, 0, 0, 0, 0, 7935
"""

class jh1600e_history:
    def __init__(self, Wh, runtime):
        self.Wh = Wh
        self.run_minutes = runtime
    
    def __repr__(self):
        return '{0},{1}'.format(self.Wh, self.run_minutes)
        
class jh1600e_stats:
    
    def __init__(self):
        self.status = "N/A"
        self.reconnected_time= ""
        self.display_fw_rev = ""
        self.display_fw_date = ""
        self.DSP_fw_rev = ""
        self.DSP_fw_date = ""
        self.redundant_fw_rev = ""
        self.redundant_fw_date = ""
        self.DC_input_voltage = ""
        self.DC_input_current = ""
        self.DC_input_power = ""
        self.insulation_resistance = ""
        self.temp_choke = ""
        self.temp_dctodc = ""
        self.temp_heatsink = ""
        self.temp_ambient = ""
        self.AC_voltage = ""
        self.AC_current = ""
        self.AC_power = ""
        self.AC_frequency = ""
        self.redundant_voltage = ""
        self.redundant_frequency = ""
        self.today_Wh = ""
        self.today_runtime = ""
        self.total_Wh = ""
        self.total_runtime = ""
        self.offline_count = ""
        self.events = ['','','','','','','','','','','','','','','','']
        self.history = ['','','','','','','']

        self.read_groups= 0
    
    def __repr__(self):  
        r =  'status {0}\n'.format(self.status) + \
        'reconnected_time {0}\n'.format(self.reconnected_time) + \
        'display_fw_rev {0}\n'.format(self.display_fw_rev) + \
        'display_fw_date {0}\n'.format(self.display_fw_date) + \
        'DSP_fw_rev {0}\n'.format(self.DSP_fw_rev) + \
        'DSP_fw_date {0}\n'.format(self.DSP_fw_date) + \
        'redundant_fw_rev {0}\n'.format(self.redundant_fw_rev) + \
        'redundant_fw_date {0}\n'.format(self.redundant_fw_date) + \
        'DC_input_voltage {0} V\n'.format(self.DC_input_voltage) + \
        'DC_input_current {0} A\n'.format(self.DC_input_current) + \
        'DC_input_power {0} W\n'.format(self.DC_input_power) + \
        'insulation_resistance {0} K ohm\n'.format(self.insulation_resistance) + \
        'temp_choke {0} C\n'.format(self.temp_choke) + \
        'temp_dctodc {0} C\n'.format(self.temp_dctodc) + \
        'temp_heatsink {0} C\n'.format(self.temp_heatsink) + \
        'temp_ambient {0} C\n'.format(self.temp_ambient) + \
        'AC_voltage {0} V\n'.format(self.AC_voltage) + \
        'AC_current {0} A\n'.format(self.AC_current) + \
        'AC_power {0} W\n'.format(self.AC_power) + \
        'AC_frequency = {0} Hz\n'.format(self.AC_frequency) + \
        'redundant_voltage {0} V\n'.format(self.redundant_voltage) + \
        'redundant_frequency {0} Hz\n'.format(self.redundant_frequency) + \
        'today_Wh {0} Wh\n'.format(self.today_Wh) + \
        'today_runtime {0:.2f} Hours\n'.format(float(self.today_runtime)/60.0) + \
        'total_Wh {0} KWh\n'.format(float(self.total_Wh)/1000.0) + \
        'offline count {0}\n'.format(self.offline_count) + \
        'total_runtime {0:.2f} Hours\n'.format(float(self.total_runtime)/60.0) + \
        'events {0}\n'.format(self.events) 
        
        #for i in range(0,7):
        #    r = r + 'Day {0}, {1} Wh, {2:.2f} Hours\n'.format(i, self.history[i].Wh, self.history[i].run_minutes/60.0)
        return r
        
    def dbg_print(self,  idx,  val):
        print '{0} - {1:05}, {1:04X}'.format(idx,  val) 

    def parse_dynamic(self,  response):
        
        #x =0
        #for i in response:
        #    self.dbg_print (x, i)                   
        #    x=x+1
            
        self.display_fw_rev = 'V{0:02}.{1:02}'.format(response[8]>>8,  response[8] & 0xFF)
        self.display_fw_date = 'Y{0:02}W{1:02}'.format(response[9]>>8,  response[9] & 0xFF)
        self.DSP_fw_rev = 'V{0:02}.{1:02}'.format(response[10]>>8,  response[10] & 0xFF)
        self.DSP_fw_date = 'Y{0:02}W{1:02}'.format(response[11]>>8,  response[11] & 0xFF)
        self.redundant_fw_rev = 'V{0:02}.{1:02}'.format(response[12]>>8,  response[12] & 0xFF)
        self.redundant_fw_date = 'Y{0:02}W{1:02}'.format(response[13]>>8,  response[13] & 0xFF)
        self.temp_choke = '{0}'.format(response[48])
        self.temp_dctodc= '{0}'.format(response[49])
        self.temp_heatsink = '{0}'.format(response[50])
        self.temp_ambient = '{0}'.format(response[51])
        self.offline_count = '{0}'.format(response[72])

        if response[16] == 0:
            self.status = 'Off'
        else:
            self.status = 'On'
        
        if response[24] == 48:
            self.read_groups = self.read_groups | 1
            #print 'Group 1 DC'
            
            self.DC_input_voltage = '{0}'.format(response[25] / 10.0)
            self.DC_input_current= '{0}'.format(response[26] / 100.0)
            self.DC_input_power= '{0}'.format(response[27])
            self.insulation_resistance= '{0}'.format(response[39])
            
            x = 57
            for i in range(x,x+8):
                if ((response[i] != 0xFFFF) & (response[i] != 0x00FF)):
                    self.events[i-x] = '{0:c}{1:02}'.format(response[i] >>8,  response[i] & 0xFF)
                
        elif response [24] == 2:
            self.read_groups = self.read_groups | 2
            #print 'Group 2 AC'
            
            self.AC_voltage = '{0}'.format(response[25] / 10.0)
            self.AC_current= '{0}'.format(response[26] / 100.0)
            self.AC_power= '{0}'.format(response[27])
            self.AC_frequency= '{0}'.format(response[28] / 100.0)
            self.redundant_voltage= '{0}'.format(response[30] / 10.0)
            self.redundant_frequency= '{0}'.format(response[31] / 100.0)
            self.today_Wh = '{0}'.format(response[41])
            self.today_runtime = '{0}'.format(response[43])
            i = (response[44] << 16) + response[45]
            self.total_Wh = '{0}'.format(i) 
            i = (response[46] << 16) + response[47]
            self.total_runtime = '{0}'.format(i) 
            
            x = 57
            for i in range(x,x+8):
                if ((response[i] != 0xFFFF) & (response[i] != 0x00FF)):
                    self.events[(i-x)+8] = '{0:c}{1:02}'.format(response[i] >>8,  response[i] & 0xFF)
            
    def parse_history(self,  response):
        for i in range(0,7):
            self.history[i] = jh1600e_history(response[i*4], response[(i*4)+2])

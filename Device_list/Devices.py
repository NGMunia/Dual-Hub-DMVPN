
from login import password, Username, enable_password


HQ_routers = {
             'R1_HUB': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'172.16.255.1'
                       },
             'R2_HUB': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'172.16.255.2'
                       }
           }
Region_A = {
             'R3': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'192.168.0.2',
                         'ip':'192.168.1.2'
                       },
             'R4': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'192.168.0.3',
                         'ip':'192.168.1.3'
                       }
            }
Region_B =  {
             'R5': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'192.168.0.4',
                         'ip':'192.168.1.4'
                       },
              'R6': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'192.168.0.5',
                         'ip':'192.168.1.5'
                       },
            }
Region_C =  {
    
          
             'R7': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'192.168.0.6',
                         'ip':'192.168.1.6'
                       },
             'R8': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'192.168.0.7',
                         'ip':'192.168.1.7'
                        } 
            }
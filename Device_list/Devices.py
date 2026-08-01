
from login import password, Username, enable_password


HQ_routers = {
             'R1_HUB': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'192.168.21.1'
                       },
             'R2_HUB': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'192.168.21.2'
                       }
           }
Region_A = {
             'R3': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'172.19.10.2',
                         'ip':'172.19.20.2'
                       },
             'R4': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'172.19.10.3',
                         'ip':'172.19.20.3'
                       }
            }
Region_B =  {
             'R5': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'172.19.10.4',
                         'ip':'172.19.20.4'
                       },
              'R6': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'172.19.10.5',
                         'ip':'172.19.20.5'
                       },
            }
Region_C =  {
    
          
             'R7': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'172.19.10.6',
                         'ip':'172.19.20.6'
                       },
             'R8': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'172.19.10.7',
                         'ip':'172.19.20.7'
                        } 
            }
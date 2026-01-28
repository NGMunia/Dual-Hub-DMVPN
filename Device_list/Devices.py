
from login import password, Username, enable_password


HQ_routers = {
             'R1_HUB': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'10.0.0.2'
                       },
             'R2_HUB': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'10.0.0.6'
                       }
           }
Region_A = {
             'R3': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'192.168.10.1'
                       },
             'R4': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'192.168.11.1'
                       }
            }
Region_B =  {
             'R5': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'192.168.20.1'
                       },
              'R6': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'192.168.21.1'
                       },
            }
Region_C =  {
    
          
             'R7': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'192.168.30.1'
                       },
             'R8': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'192.168.31.1'
                        } 
            }
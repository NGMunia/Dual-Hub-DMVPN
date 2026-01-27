
from login import password, Username, enable_password


Routers = {
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
                       },
             'R1_BR1': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'192.168.10.1'
                       },
             'R2_BR2': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'192.168.20.1'
                       }, 
             'R3_BR3': {
                         'device_type':'cisco_ios',
                         'username':Username,
                         'password': password,
                         'secret':enable_password,
                         'ip':'192.168.30.1'
                       }               
          }
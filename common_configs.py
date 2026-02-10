from netmiko import ConnectHandler
from Device_list.Devices import HQ_routers, Region_A, Region_B, Region_C
from jinja2 import FileSystemLoader, Environment
from itertools import chain



## SNMP CONFIGURATION
# Define the IP address of the NMS server where SNMP traps will be sent

snmp_server = input("What is the IP address of NMS server? ")
jinja_templates = input('Input directory path:')  

for devices in chain(
                     HQ_routers.values(),
                     Region_A.values(), 
                     Region_B.values(), 
                     Region_C.values()
                     ):
  c = ConnectHandler(**devices)
  c.enable()

  data = {
           'snmp_server_ip':snmp_server 
         } 

  env = Environment(loader=FileSystemLoader(jinja_templates))
  template = env.get_template("snmp.j2")
  
  commands = template.render(data).splitlines()
  print(c.send_config_set(commands))



## DISABLING LLDP AND CPD ON INTERNET FACING INTERFACES:

for devices in chain(
                     Region_A.values(),
                     Region_B.values(),
                     Region_C.values(),
                     HQ_routers.values()
                    ):
    c = ConnectHandler(**devices)
    c.enable()

    commands = ['interface e0/3',
                'no cdp enable',
                'no lldp transmit']
    print(c.send_config_set(commands),'\n')
    c.save_config()
    c.disconnect()
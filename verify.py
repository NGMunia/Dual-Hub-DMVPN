
from Device_list.Devices import HQ_routers, Region_A, Region_B, Region_C
from netmiko import ConnectHandler
from itertools import chain


## VERIFYING EIGRP NEIGHBORSHIP ON mGRE TUNNELS:
for devices in chain(
                     HQ_routers.values(),
                     Region_A.values(), 
                     Region_B.values(), 
                     Region_C.values()
                     ):
  c = ConnectHandler(**devices)
  c.enable()
  hostname = c.send_command('show version', use_textfsm=True)[0]['hostname']
  
  output = c.send_command('show ip eigrp neighbors\n')
  print(f'\n\n{hostname}\n,{output}')



## VERIFYING NHRP
for devices in chain(
                     HQ_routers.values(),
                     Region_A.values(), 
                     Region_B.values(), 
                     Region_C.values()
                     ):
  c = ConnectHandler(**devices)
  c.enable()
  hostname = c.send_command('show version', use_textfsm=True)[0]['hostname']
  
  output = c.send_command('show ip nhrp\n')
  print(f'\n\n{hostname}\n,{output}')



#VERIFYING EIGRP ROUTES:
for devices in chain(
                     HQ_routers.values(),
                     Region_A.values(), 
                     Region_B.values(), 
                     Region_C.values()
                     ):
  c = ConnectHandler(**devices)
  c.enable()
  hostname = c.send_command('show version', use_textfsm=True)[0]['hostname']
  
  output = c.send_command('show ip route eigrp','\n')
  print(f'\n\n{hostname}\n,{output}')



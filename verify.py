
from Device_list.Devices import HQ_routers, Region_A, Region_B, Region_C
from netmiko import ConnectHandler
from itertools import chain


for devices in chain(
                        HQ_routers.values(),
                        Region_A.values(), 
                        Region_B.values(), 
                        Region_C.values()
                     ):
      try:
          c = ConnectHandler(**devices)
          c.enable()
          hostname = c.send_command('show version', use_textfsm=True)[0]['hostname']
          print(f'Connecting to {hostname} gateway.....')
 # Veryifying EIGRP neighborship:     
          print(f'Verifying EIGRP neighbors of {hostname} gateway......')
          output = c.send_command('show ip eigrp neighbors\n')
          print(f'\n\n{hostname}\n,{output}')
      except Exception as e:
          print(f'Error, {e}')
          exit()


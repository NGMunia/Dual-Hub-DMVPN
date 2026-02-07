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



# CONFIGURING MOTD BANNER:
# - This is the welcome banner you see when you login remotely on the device:
print('CONFIGURING MOTD BANNER')
for devices in chain(
                     HQ_routers.values(),
                     Region_A.values(), 
                     Region_B.values(), 
                     Region_C.values()
                     ):
    
    c = ConnectHandler(**devices)
    c.enable()
    host = c.send_command('show version',use_textfsm=True)[0]['hostname']
    banner_hostname = input (f'Enter the new hostname of {host}: ')

    commands = [
                'banner login @',
               f'{"#"*50}',
               f'{"#  "}{banner_hostname}',
               f'{"#  "}ROYAL MEDIA SERVICES LIMITED',
               f'{"#  "}BROADCAST TRANSMISSION DEPARTMENT',
               f'{"#  "}Unauthorized access is strictly forbidden',
               f'{"#"*50}',
               '@']
    print(c.send_config_set(commands),'\n')
    c.save_config()
    c.disconnect()




# CONFIGURING CRYPTO-ALGORITHMS:
#  These are the parameters that will be used for IKE phase 1 and IKE phase 2 Negotiations;
jinja_templates = input('Input directory path:')  
IKE_policy_number = input('Input IKE policy number: ')

for devices in chain(
                     HQ_routers.values(),
                     Region_A.values(), 
                     Region_B.values(), 
                     Region_C.values()
                     ):
  c = ConnectHandler(**devices)
  c.enable() 

  data = {
           'IKE_policy_number': IKE_policy_number
         } 

  env = Environment(loader=FileSystemLoader(jinja_templates))
  template = env.get_template("crypto.j2")
  
  commands = template.render(data).splitlines()
  print(c.send_config_set(commands))

  

## CONFIGURE LAN IPs
for devices in chain(
                     Region_A.values(), 
                     Region_B.values(), 
                     Region_C.values()
                     ):
     c = ConnectHandler(**devices)
     c.enable()
     hostname = c.send_command('show version', use_textfsm=True)[0]['hostname']

     ip = input(f'Input the LAN Gateway IP address and subnet mask of {hostname}: ')
     intf = input('LAN interface: ')

     commands = [f'interface {intf}',
                 f'ip address {ip}',
                 'no shut'
                ]
     
     print(c.send_config_set(commands),'\n')
     c.save_config()
     c.disconnect()


## ADVERTISING NEW NETWORKS ON EIGRP AS
for devices in chain(
                     Region_A.values(), 
                     Region_B.values(), 
                     Region_C.values()
                     ):
     c = ConnectHandler(**devices)
     c.enable()
     hostname = c.send_command('show version', use_textfsm=True)[0]['hostname']

     network = input(f'Input the LAN network and wildcard mask of {hostname}: ')

     commands = ['router eigrp EIGRP',
                 'address-family ipv4 autonomous-system 100',
                 f'network {network}'
                ]
     
     print(c.send_config_set(commands),'\n')
     c.save_config()
     c.disconnect()
    

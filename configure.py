
from Device_list.Devices import HQ_routers, Region_A, Region_B, Region_C
from itertools import chain
from netmiko import ConnectHandler
from jinja2 import FileSystemLoader, Environment


print('Accessing the Jinja Templates........')
jinja_templates = input('select the directory path of the Jinja Template used for configurations: ')

# Configuring SNMP on HQ routers:
for devices in chain(HQ_routers.values()):
    c = ConnectHandler(**devices)
    c.enable()

    hostname = c.send_command('show version', use_textfsm=True)[0]['hostname']
    print(f'Successfully Connected to {hostname} Gateway!')

    print('-----Configuring SNMP----')
    snmp_server = input('What is the IP address of SNMP Server?  ')
    snmp_intf = input('What is the SNMP traps source interface? ')
    chassis_id = c.send_command('show version', use_textfsm=True)[0]['hostname']
    
    data = {
             'snmp_server_ip':snmp_server,
             'snmp_interface':snmp_intf,
             'chassis_id':chassis_id 
            } 
    
    env = Environment(loader=FileSystemLoader(jinja_templates))
    template = env.get_template("snmp.j2") 
    snmp_commands = template.render(data).splitlines()
    print(c.send_config_set(snmp_commands))



# CONFIGURING MOTD BANNER:
# - This is the welcome banner you see when you login remotely on the device:
    print('-----CONFIGURING MOTD BANNER-----')
    banner_commands = [ 
                         'banner login @',
                        f'{"#"*50}',
                        f'{"#  "}{chassis_id}',
                        f'{"#  "}BROADCAST MEDIA SERVICES LTD',
                        f'{"#  "}BROADCAST TRANSMISSION DEPARTMENT',
                        f'{"#  "}Unauthorized access is strictly forbidden',
                        f'{"#"*50}',
                        '@'
                      ]
    print(c.send_config_set(banner_commands),'\n')
    c.save_config()
    c.disconnect()

from Device_list.Devices import HQ_routers, Region_A, Region_B, Region_C
from netmiko import ConnectHandler
from itertools import chain
from csv import writer



# DEVICE DOCUMENTATION

filepath = input('input the folder path where device inventory will be stored: ')
with open(f'{filepath}/Data.csv','w') as f:
    write_data = writer(f)
    write_data.writerow(['Hostname','IP-Address','Software-Image','Version','Serial-No','Hardware'])
    for Devices in chain(HQ_routers.values(), Region_A.values(), Region_B.values(), Region_C.values()):
        conn = ConnectHandler(**Devices)
        conn.enable()
        output = conn.send_command('show version',use_textfsm=True)[0]

        hostname = output['hostname']
        ip_addr  = Devices['ip']
        software = output['software_image']
        version  = output['version']
        serial   = output['serial']
        hardware = output['hardware']

        write_data.writerow([hostname,ip_addr,software,version,serial,hardware])
        conn.disconnect()
    
        print(f" Finished taking and Documenting {hostname} information" )


## DEVICE RUNNING CONFIGURATIONS:
backup_filepath = input('Input the folder path where all startup configurations will be stored: ')
for Devices in chain(HQ_routers.values(), Region_A.values(), Region_B.values(), Region_C.values()):
    c = ConnectHandler(**Devices)
    c.enable()

    hostname = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show startup-config')

    with open(f'{backup_filepath}/{hostname}', 'w') as f:
        f.write(output)
    print(f'The startup config of device {hostname} has been successfully been backed up!!!')



## Configuring SNMP

# for Devices in chain(HQ_routers.values(), Region_A.values(), Region_B.values(), Region_C.values()):
#     c = ConnectHandler(**Devices)
#     c.enable()

#     commands = [
#                 'ip access-list standard snmp_acl',
#                 'permit host 10.1.30.254',
#                 'snmp-server community device_snmp snmp_acl',
#                 'snmp-server system-shutdown',
#                 'snmp-server enable traps config',
#                 'snmp-server host 10.1.30.254 version 2c device_snmp']
#     print(c.send_config_set(commands))
       
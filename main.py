from Device_list.Devices import Routers
from netmiko import ConnectHandler
from csv import writer



## DEVICE DOCUMENTATION

filepath = input('input the folder path where device inventory will be stored: ')
with open(f'{filepath}/Data.csv','w') as f:
    write_data = writer(f)
    write_data.writerow(['Hostname','IP-Address','Software-Image','Version','Serial-No','Hardware'])
    for Devices in Routers.values():
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
for devices in Routers.values():
    c = ConnectHandler(**devices)
    c.enable()

    hostname = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show startup-config')

    with open(f'{backup_filepath}/{hostname}', 'w') as f:
        f.write(output)
    print(f'The startup config of device {hostname} has been successfully been backed up!!!')
              

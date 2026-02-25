
# SCOPE:
# The following scripts are used to back up configurations and fetch critical device health and document them for
# reference.

from Device_list.Devices import HQ_routers, Region_A, Region_B, Region_C
from netmiko import ConnectHandler
from itertools import chain
from csv import writer



# # DEVICE INVETORY
# - This script will parse all network devices and collect critical information such as: 
#     - Software information
#     - Software version
#     - Serial numbers
#     - Hardware models
#  A .csv file will then be created with the writer feature and document the values collected and
#  structued in a dict format using TextFSM



filepath = input('input the folder path where device inventory will be stored: ')
backup_filepath = input('Input the folder path where all startup configurations will be stored: ')

try:
  with open(f'{filepath}/Data.csv','w') as f:
    write_data = writer(f)
    write_data.writerow(['Hostname','IP-Address','Software-Image','Version','Serial-No','Hardware'])

    for Devices in chain(
                         HQ_routers.values(), 
                         Region_A.values(), 
                         Region_B.values(), 
                         Region_C.values()
                        ):
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
        print(f" Finished taking and Documenting {hostname} information" )

## STORING START-UP CONFIGURATIONS:
# - This cript will parse through all network devices, collect and store their start-up configurations

        output = conn.send_command('show startup-config')

        with open(f'{backup_filepath}/{hostname}', 'w') as f:
          f.write(output)
        print(f'The startup config of device {hostname} has been successfully been backed up!!!')
except Exception as e:
   print(f'Error, {e}')
   exit()



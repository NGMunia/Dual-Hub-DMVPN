from Device_list.Devices import Routers
from netmiko import ConnectHandler
from rich import print as rp
from csv import writer

'''
Inventory Device Information Documantation
'''  
with open('/home/munia/Dual-Hub-DMVPN/Inventory/Data.csv','w') as f:
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
    
    rp(f"[cyan] Finished taking and Documenting Devices' information" )

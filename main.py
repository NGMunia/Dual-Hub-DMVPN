from Device_list.Devices import Routers
from netmiko import ConnectHandler
from rich import print as rp
from csv import writer
import ntc_templates
import requests


'''
Configuring Cryptography
'''
url1  = 'http://10.1.30.100:8000/Devices/R3_BR3/Configure/Cryptography'

data1 = {'policy_number': 100}
result= requests.post(url1, json=data)
if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' Cryptography not configured!')


'''
Configuring LAN interfaces on BRANCH networks
'''
url2  = 'http://10.1.30.100:8000/Devices/R3_BR3/Configure/Interface'

data2 = {'Interface_name': 'G0/0',
         'Description': 'Branch-3-LAN',
         'Address': '192.168.30.1',
         'Netmask': '255.255.255.0'}
result= requests.post(url2, json=data2)
if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' Interface not configured!')


'''
Configuring DHCP in BRANCH networks
'''
url3  = 'http://10.1.30.100:8000/Devices/R3_BR3/Configure/DHCP'

data3 = {'START_IP':'192.168.30.1',
         'END_IP':'192.168.30.10',
         'NETWORK':'192.168.30.0',
         'NETMASK': '255.255.255.0',
         'GATEWAY':'192.168.30.1',
         'DHCP_POOL_NAME':'BRANCH-3-LAN-DHCP'}
result= requests.post(url3, json=data3)
if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' DHCP not configured!')


'''
Configuring Spoke Tunnels
'''
url4  = 'http://10.1.30.100:8000/Devices/R3_BR3/Configure/Interface/Spoke-tunnel'

data4 =  {'Tunnel_ID' : 20,
          'Description' : 'DMVPN-2-Tunnel',
          'Source': 'g0/1',
          'IP_address': '172.17.0.4',
          'Netmask' : '255.255.255.0',
          'Bandwidth' : 30000,
          'Authentication' : 'dmvpn2',
          'Network_ID' : 20,
          'NHS_IP' : '172.17.0.1',
          'NBMA_IP' : '44.67.28.2',
          'Tunnel_Key' : 20,
          'Delay' : 1 }
result= requests.post(url4, json=data4)
if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' Tunnel Interface not configured!')


'''
Configuring NAT 
'''
url5  = 'http://10.1.30.100:8000/Devices/R1_BR1/Configure/NAT'

data5 =  {'Inside_intf' : 'g0/0',
          'Outside_intf': 'g0/1',
          'NATed_IP_address' : '192.168.10.0',
          'Wildcard_Mask' : '0.0.0.255'}
result= requests.post(url5, json=data5)
if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' NAT not configured!')


'''
Configuring SNMP
'''
url6  = 'http://10.1.30.100:8000/Devices/R3_BR3/Configure/SNMP'

data6 = {'Server_IP': '10.1.20.100', 'SNMP_password': 'device_snmp'}
result= requests.post(url6, json=data6)
if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' SNMP not configured!')


'''
Configuring NetFlow
'''
url6  = 'http://10.1.30.100:8000/Devices/R3_BR3/Configure/NetFlow'

data6 = {'Flow_Interface': 'g0/0', 'Server_IP': '10.1.20.100','UDP_Port':9998}
result= requests.post(url6, json=data6)
if result.status_code == 201:
    rp('Response:',result.status_code,'\n',result.json())
else:
    rp('Response:',result.status_code,' NetFlow not configured!')


'''
Backing up Running configs
'''
for Devices in Routers.values():
    conn = ConnectHandler(**Devices)
    conn.enable()
    host = conn.send_command('show run | include hostname')
    output = conn.send_command('show run')
    with open (f'/home/munia/Dual-Hub-DMVPN/Running_Configs/{host}','w')as f:
        f.write(output)
        conn.disconnect()
    print(f'{host} Backup successful!')


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

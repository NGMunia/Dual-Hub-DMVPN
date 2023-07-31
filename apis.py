
from fastapi import FastAPI, status
from pydantic import BaseModel
from netmiko import ConnectHandler
from Device_list.Devices import Routers
from jinja2 import Environment, FileSystemLoader

app = FastAPI()

'''
CRYPTO REST-API
'''
class Crypto(BaseModel):
    policy_number : int
@app.post('/Devices/{Device_ID}/Configure/Cryptography', status_code=status.HTTP_201_CREATED)
def CryptoConfig(Device_ID:str, post:Crypto):
    device = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()

    varibles = {'Policy_Number': str(post.policy_number)}
    env  = Environment(loader=FileSystemLoader('/home/munia/Dual-Hub-DMVPN/Jinja_templates'))
    template = env.get_template('Cryptography.j2')

    commands = template.render(varibles)
    result = conn.send_config_set(commands.splitlines())
    conn.save_config()
    conn.disconnect()
    return result.splitlines()

'''
DHCP REST-API
'''
class DHCPClass(BaseModel):
    START_IP : str
    END_IP : str
    NETWORK : str
    NETMASK : str
    GATEWAY: str
    DHCP_POOL_NAME : str
@app.post('/Devices/{Device_ID}/Configure/DHCP', status_code=status.HTTP_201_CREATED)
def dhcpconfig(Device_ID:str, post:DHCPClass):
    device = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()

    variables = {'START_IP': post.START_IP,'END_IP': post.END_IP,'NETWORK': post.NETWORK,
                 'NETMASK': post.NETMASK,'GATEWAY': post.GATEWAY, 'DHCP_POOL_NAME':post.DHCP_POOL_NAME}
    env = Environment(loader=FileSystemLoader('/home/munia/Dual-Hub-DMVPN/Jinja_templates'))
    template = env.get_template('DHCP.j2')

    commands = template.render(variables)
    result = conn.send_config_set(commands.splitlines())
    conn.save_config()
    conn.disconnect()
    return result.splitlines()

'''
NETFLOW REST-API
'''
class NetFlowclass(BaseModel):
    Flow_Interface : str
    Server_IP : str
    UDP_Port : int
@app.post('/Devices/{Device_ID}/Configure/NetFlow', status_code=status.HTTP_201_CREATED)
def dhcpconfig(Device_ID:str, post:NetFlowclass):
    device = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()

    varibles = {'Flow_Interface': post.Flow_Interface, 'Server_IP': post.Server_IP,
                'UDP_Port': str(post.UDP_Port)}
    env = Environment(loader=FileSystemLoader('/home/munia/Dual-Hub-DMVPN/Jinja_templates'))
    template = env.get_template('NetFlow.j2')

    commands = template.render(varibles)
    result = conn.send_config_set(commands.splitlines())
    conn.save_config()
    conn.disconnect()
    return result.splitlines()

'''
INTERFACE REST-API
'''
class Intflass(BaseModel):
    Interface_name : str
    Description : str
    Address : str
    Netmask : str
@app.post('/Devices/{Device_ID}/Configure/Interface', status_code=status.HTTP_201_CREATED)
def dhcpconfig(Device_ID:str, post:Intflass):
    device = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()

    varibles = {'Interface_name': post.Interface_name, 'Description': post.Description,
                'Address': post.Address, 'Netmask': post.Netmask}
    env = Environment(loader=FileSystemLoader('/home/munia/Dual-Hub-DMVPN/Jinja_templates'))
    template = env.get_template('Interface.j2')

    commands = template.render(varibles)
    result = conn.send_config_set(commands.splitlines())
    conn.save_config()
    conn.disconnect()
    return result.splitlines()   

'''
SPOKE TUNNEL REST-API
'''
class spokeclass(BaseModel):
    Tunnel_ID : int
    Description : str
    Source: str
    IP_address: str
    Netmask : str
    Authentication : str
    Network_ID : int
    NHS_IP : str
    NBMA_IP : str
    Tunnel_Key : int
    Delay : int
@app.post('/Devices/{Device_ID}/Configure/Interface/Spoke-tunnel', status_code=status.HTTP_201_CREATED)
def dhcpconfig(Device_ID:str, post:spokeclass):
    device = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()

    varibles = {'Tunnel_ID': str(post.Tunnel_ID), 'Description': post.Description,'Source':post.Source,
                'IP_address': post.IP_address, 'Netmask': post.Netmask,'Authentication': post.Authentication, 
                'Network_ID': str(post.Network_ID),
                'NHS_IP': str(post.NHS_IP),'NBMA_IP':str(post.NBMA_IP),'Tunnel_key': str(post.Tunnel_Key),
                'Delay':str(post.Delay)}
    env = Environment(loader=FileSystemLoader('/home/munia/Dual-Hub-DMVPN/Jinja_templates'))
    template = env.get_template('Spoke_tunnel.j2')

    commands = template.render(varibles)
    result = conn.send_config_set(commands.splitlines())
    conn.save_config()
    conn.disconnect()
    return result.splitlines()   

'''
NAT REST-API
'''
class NATclass(BaseModel):
    Inside_intf : str
    Outside_intf : str
    NATed_IP_address : str
    Wildcard_Mask : str
@app.post('/Devices/{Device_ID}/Configure/NAT', status_code=status.HTTP_201_CREATED)
def dhcpconfig(Device_ID:str, post:NATclass):
    device = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()

    varibles = {'Inside_intf':post.Inside_intf,'Outside_intf':post.Outside_intf,
                'NATed_IP_address':post.NATed_IP_address,'Wildcard_Mask': post.Wildcard_Mask}
    env = Environment(loader=FileSystemLoader('/home/munia/Dual-Hub-DMVPN/Jinja_templates'))
    template = env.get_template('NAT.j2')

    commands = template.render(varibles)
    result = conn.send_config_set(commands.splitlines())
    conn.save_config()
    conn.disconnect()
    return result.splitlines()   

'''
NTP REST-API
'''
class NTPClass (BaseModel):
    ntp_server : str
@app.post('/Devices/{Device_ID}/Configure/NTP', status_code = status.HTTP_201_CREATED)
def ntp_config(post: NTPClass, Device_ID: str):
    device = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()

    varibles = {'ntp_server':post.ntp_server}
    env = Environment(loader=FileSystemLoader('/home/munia/Dual-Hub-DMVPN/Jinja_templates'))
    template = env.get_template('NTP.j2')

    commands = template.render(varibles)
    result = conn.send_config_set(commands.splitlines())
    conn.save_config()
    conn.disconnect()
    return result.splitlines()   

'''
SNMP REST-API
'''
class SNMPclass(BaseModel):
    Server_IP : str
    SNMP_password : str
@app.post('/Devices/{Device_ID}/Configure/SNMP', status_code = status.HTTP_201_CREATED)
def SNMPconfig(post: SNMPclass, Device_ID: str):
    device = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()

    varibles = {'Server_IP':post.Server_IP, 'SNMP_password': post.SNMP_password}
    env = Environment(loader=FileSystemLoader('/home/munia/Dual-Hub-DMVPN/Jinja_templates'))
    template = env.get_template('SNMP.j2')

    commands = template.render(varibles)
    result   = conn.send_config_set(commands.splitlines())
    conn.save_config()
    conn.disconnect()
    return result.splitlines()   


'''
Zone-based Firewall
'''
class ZBFclass(BaseModel):
    protocol_list : list
    Inside_intf : list
    Outside_intf : list
@app.post('/Devices/{Device_ID}/Configure/ZBF', status_code = status.HTTP_201_CREATED)
def ZBFconfig(post: ZBFclass, Device_ID: str):
    device = Routers[Device_ID]
    conn = ConnectHandler(**device)
    conn.enable()

    variables = {'protocol_list': post.protocol_list, 'Inside_intf': post.Inside_intf, 
                 'Outside_intf': post.Outside_intf}
    env = Environment(loader=FileSystemLoader('/home/munia/Dual-Hub-DMVPN/Jinja_templates'))
    template = env.get_template('ZBF.j2')

    commands = template.render(variables)
    result  = conn.send_config_set(commands.splitlines())
    conn.save_config()
    conn.disconnect()
    return result.splitlines()


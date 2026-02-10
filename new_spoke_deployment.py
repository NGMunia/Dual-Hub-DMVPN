
# NEW SPOKE DEPLOYMENT
# Prerequisites: 
#  - The hub routers' static public IPs should be known for NHRP packets exchange
#  - The new spoke out of the box must be configured for SSH remote connection
#  - The login credentials must be configured as those in the login  script, to ensure consistency across board
#  - A default route must be configured
#  - (Optional) A unique hostname may be configured.



from login import password, Username, enable_password
from netmiko import ConnectHandler
from jinja2 import FileSystemLoader, Environment



hostname = input('Specify the Hostname of the new spoke: ')
public_ip = input('What is the public IP on the new router: ')
new_spoke =  {
                  'device_type':'cisco_ios',
                  'username':Username,
                  'password': password,
                  'secret':enable_password,
                  'ip': public_ip
              } 

c = ConnectHandler(**new_spoke)
c.enable()

tunnel0_ip = input('Whats the IP address of tunnel0? ')
tunnel1_ip = input('Whats the IP address of tunnel1? ')
tunnel0_source_IP = input('whats the tunnel source IP/interface? ')

data = {
        'tunnel0_ip':tunnel0_ip,
        'tunnel1_ip':tunnel1_ip,
        'tunnel0_source_ip':tunnel0_source_IP
        }
jinja_templates = input('Input directory path:')
env = Environment(loader=FileSystemLoader(jinja_templates))
template = env.get_template("spoke.j2")
hostname_commands = [f'hostname {hostname}']
commands = template.render(data).splitlines()
print(c.send_config_set(hostname_commands))
print('\n')
print(c.send_config_set(commands))

## CONFIGURE NEW LAN IPs
# - This script will configure LAN IP(s) of the new spoke deployed.
# - Specify the correct IP and subnet mask.

ip = input(f'Input the LAN IP address and subnet mask whose gateway is {hostname}: ')
intf = input('LAN interface: ')

intf_commands = [
            f'interface {intf}',
            f'ip address {ip}',
            'no shut'
           ]
     
print(c.send_config_set(intf_commands),'\n')

## ADVERTISING NEW NETWORKS ON EIGRP AS:
# - This script will configure EIGRP to advertise the new subnets on the new spoke deployed:
# - The right network and wildcard mask is critical.
                     
network = input(f'Input the LAN network and wildcard mask attached to {hostname} you wish to advertise: ')
eigrp_commands = [
                  'router eigrp EIGRP',
                  'address-family ipv4 autonomous-system 100',
                  f'network {network}'
                 ]    
print(c.send_config_set(eigrp_commands),'\n')
c.save_config()
c.disconnect()
    
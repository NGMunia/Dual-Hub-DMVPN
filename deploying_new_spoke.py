
# NEW SPOKE DEPLOYMENT
# Prerequisites: 
#  - The hub routers' static public IPs should be known for NHRP packets exchange
#  - The new spoke out of the box must be configured for SSH remote connection
#  - The login credentials must be configured as those in the login  script, to ensure consistency across board
#  - A default static route pointing to the ISP must be configured
#  - (Optional) A unique hostname may be configured.



from login import password, Username, enable_password
from netmiko import ConnectHandler
from jinja2 import FileSystemLoader, Environment

#  Accessing the Public IP of the new Spoke
print('----CONNECTING TO THE NEW SPOKE-----')
public_ip = input(f'What is the public IP address configured on the new spoke? ')
new_spoke =  {
                  'device_type':'cisco_ios',
                  'username':Username,
                  'password': password,
                  'secret':enable_password,
                  'ip': public_ip
             } 
c = ConnectHandler(**new_spoke)
c.enable()

hostname = c.send_command('show version', use_textfsm=True)[0]['hostname']

# Configuring the DMVPN tunnels:
print('-----CONFIGURING THE TUNNELS OF THE NEW SPOKE-----')
tunnel0_ip = input(f'Whats the IP address of tunnel0 of {hostname}?  ')
tunnel1_ip = input(f'Whats the IP address of tunnel1 of {hostname}?  ')
tunnel0_source_IP = input('whats the tunnel source IP/interface? ')

data = {
        'tunnel0_ip':tunnel0_ip,
        'tunnel1_ip':tunnel1_ip,
        'tunnel0_source_ip':tunnel0_source_IP
       }

jinja_templates = input('select the directory path of the Jinja Template used for configurations: ')
env = Environment(loader=FileSystemLoader(jinja_templates))
template = env.get_template("spoke.j2")
commands = template.render(data).splitlines()
print(c.send_config_set(commands))


# CONFIGURE NEW LAN IPs
# - This script will configure LAN IP(s) of the new spoke deployed.
# - Specify the correct IP and subnet mask.
print('-----CONFIGURING LAN IP AND SUBNET MASK-----')
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
print('-----CONFIGURING EIGRP----')                    
lan_network = input(f'Input the LAN network and wildcard mask attached to {hostname} you wish to advertise: ')
eigrp_commands = [
                   'router eigrp EIGRP',
                   'address-family ipv4 autonomous-system 100',
                   'af-interface default',
                   'bandwidth-percent 25',
                  f'network {lan_network}',
                   'network 192.168.1.0',
                   'network 192.168.0.0'
                 ]    
print(c.send_config_set(eigrp_commands),'\n')


# CONFIGURING MOTD BANNER:
# - This is the welcome banner you see when you login remotely on the device:
print('-----CONFIGURING MOTD BANNER-----')
banner_commands = [ 
                    'banner login @',
                   f'{"#"*50}',
                   f'{"#  "}{hostname}',
                   f'{"#  "}ROYAL MEDIA SERVICES LIMITED',
                   f'{"#  "}BROADCAST TRANSMISSION DEPARTMENT',
                   f'{"#  "}Unauthorized access is strictly forbidden',
                   f'{"#"*50}',
                    '@'
                  ]
print(c.send_config_set(banner_commands),'\n')


## Configuring Cryptography:
# - This script configures IPsec over DMVPN tunnels.
print('------CONFIGURING CRYPTOGRAPHY (IPSEC)-----')
IKE_policy_number = input('Input IKE policy number: ')
crypto_data = {
                'IKE_policy_number': IKE_policy_number
              } 
env = Environment(loader=FileSystemLoader(jinja_templates))
template = env.get_template("crypto.j2")
  
crypto_commands = template.render(crypto_data).splitlines()
print(c.send_config_set(crypto_commands))


## SAVE ALL CONFIGURATIONS:
print('Saving all configurations....')
c.save_config()
c.disconnect()
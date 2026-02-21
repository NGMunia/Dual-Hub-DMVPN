


# NEW SPOKE DEPLOYMENT
# Prerequisites: 
#  - The hub routers' static public IPs should be known for NHRP packets exchange
#  - The new spoke out of the box must be configured for SSH remote connection
#  - The login credentials must be configured as those in the login  script, to ensure consistency across board
#  - A default static route pointing to the ISP must be configured
#  - A public IP must be configured statically or dynamically assigned to a known interface for reachability
#  - (Optional) A unique hostname may be configured.



from login import password, Username, enable_password
from netmiko import ConnectHandler
from jinja2 import FileSystemLoader, Environment
import ipaddress



# What is try and except?
# try and except are Python’s way of handling errors safely.
# Instead of the script crashing when something goes wrong, it can catch the error and you decide what to do.
#     try:
#         # Code that might fail
#     except:
#         # This runs instead of crashing


# ACCESSING THE NEW SPOKE...........
print('Connecting to the new SPOKE........')
while True:
    try:
        public_ip = input(f'What is the public IP address configured on the new spoke? ')
        ipaddress.IPv4Address(public_ip)
        break
    except ValueError:
        print('Invalid IP address!!')           
new_spoke =  {
                  'device_type':'cisco_ios',
                  'username':Username,
                  'password': password,
                  'secret':enable_password,
                  'ip': public_ip
             } 
try:
    c = ConnectHandler(**new_spoke)
    c.enable()
    hostname = c.send_command('show version', use_textfsm=True)[0]['hostname']
    print(f'Successfully Connected to {hostname} Gateway!')


# Accessing the Jinja Templates
    print('Accessing the Jinja Templates........')
    jinja_templates = input('select the directory path of the Jinja Template used for configurations: ')
    env = Environment(loader=FileSystemLoader(jinja_templates))


# Configuring the DMVPN tunnels:
    print('-----CONFIGURING THE TUNNELS OF THE NEW SPOKE-----')
    while True:
        try: 
            tunnel0_source_IP = input(f'whats the tunnel source IP/interface of {hostname} gateway? ')

            tunnel0_ip = input(f'Whats the IP address of tunnel0 of {hostname} gateway?  ')
            ipaddress.IPv4Address(tunnel0_ip)
        
            tunnel1_ip = input(f'Whats the IP address of tunnel1 of {hostname} gateway?  ')
            ipaddress.IPv4Address(tunnel1_ip)
            break
        except ValueError:
            print('Invalid IP address used!!')

    data = {
              'tunnel0_ip':tunnel0_ip,
              'tunnel1_ip':tunnel1_ip,
              'tunnel0_source_ip':tunnel0_source_IP
           }
  
    template = env.get_template("spoke.j2")
    commands = template.render(data).splitlines()
    print(c.send_config_set(commands))



# CONFIGURE NEW LAN IPs
# - This script will configure LAN IP(s) of the new spoke deployed.
# - Specify the correct IP and subnet mask.
    print('-----CONFIGURING LAN IP AND SUBNET MASK-----')
    while True:
        try:
          ip = input(f'Input the /24 LAN IP address whose gateway is {hostname}: ')
          ipaddress.IPv4Address(ip)
          break
        except ValueError:
          print('Invalid IP address!!')
    intf = input('LAN interface: ')
    intf_commands = [
                      f'interface {intf}',
                      f'ip address {ip} 255.255.255.0',
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


## Configuring Cryptography:
# - This script configures IPsec over DMVPN tunnels.
    print('------CONFIGURING CRYPTOGRAPHY (IPSEC)-----')
    IKE_policy_number = input('Input IKE policy number: ')
    crypto_data = {'IKE_policy_number': IKE_policy_number} 

    env = Environment(loader=FileSystemLoader(jinja_templates))
    template = env.get_template("crypto.j2")
    crypto_commands = template.render(crypto_data).splitlines()
    print(c.send_config_set(crypto_commands))

    

# Configuring SNMP SERVER
# - This script configures the NMS server where SNMP traps will be sent.
    print('-----Configuring SNMP server on the spoke-----')
    snmp_server = input('What is the IP address of SNMP Server?  ')
    data = {'snmp_server_ip':snmp_server } 

    env = Environment(loader=FileSystemLoader(jinja_templates))
    template = env.get_template("snmp.j2") 
    snmp_commands = template.render(data).splitlines()
    print(c.send_config_set(snmp_commands))


# Disbaling CDP and LLPD on internet-facing Links:
# - This script disables neigbor discovery from the internet.
    print('----Disabling CDP and LLDP on internet-facing links-----')
    cdp_commands = [
                     f'interface {tunnel0_source_IP}',
                      'no cdp enable',
                      'no lldp transmit'
                   ]
    print(c.send_config_set(cdp_commands),'\n')


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

## SAVE ALL CONFIGURATIONS:
# -This will save all the configurarions;
    print('Saving all configurations....')
    print('THE SPOKE HAS BEEN SUCCESSFULLY DEPLOYED TO THE DMVPN NETWORK!')
    c.save_config()
    c.disconnect()



# Displays errors encountered while running the script
except TimeoutError:
    print(f'Connection Timeout!!! Check if the IP {public_ip} is reachable and SSH is enabled!! ')
    exit()
except Exception as e:
    print(f'Connection Error, {e}')
    exit()








 
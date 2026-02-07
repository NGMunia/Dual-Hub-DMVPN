

from login import password, Username, enable_password
from netmiko import ConnectHandler
from jinja2 import FileSystemLoader, Environment

# NEW SPOKE DEPLOYMENT
# Prerequisites: 
#  - The hub routers' static public IPs should be known for NHRP packets exchange
#  - The new spoke out of the box must be configured for SSH remote connection
#  - The login credentials must be configured as those in the login  script, to ensure consistency across board
#  - A default route must be configured

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
commands = template.render(data).splitlines()
print(c.send_config_set(commands))


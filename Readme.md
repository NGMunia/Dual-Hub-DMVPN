DUAL-HUB/CLOUD DMVPN WITH IPSEC:
-----------------------------------------------------------------------------------------

  - EIGRP is used for reachability among the Branches and HQ
  - The topology leverages EIGRP's ECMP to load-share traffic on both tunnels.
  - Base configuration for the NBMA/Transoport networks has been done using CLI
  - IPsec Secures the DMVPN tunnels.
  - Common (Repetitve) Configurations have been implemented using Automation.
      - Jinja2 has been used as a framework to construct configuration templates.
      - FastAPI has been used to construct simple REST-APIs as the NBI
      - Netmiko leverages SSH as its SBI to interact with network devices.
      - REST-APIs are enabled for the following tasks:
          - IPsec Cryptography variables
          - DHCP
          - Interface configuration
          - Spoke tunnel Configuration
          - SNMP,NetFlow, NTP, NAT
          - Zone-based Firewall
          
      - Python scripts have been written for the follwing tasks:
          - Backing up running configs
          - Inventory that Device information collection and Documentation.

  - IPSLA with object tracking has been configured on R1-LAN to track default route
    to the internet with R1-HUB being the preferred default route.
  
  - Each branch site has its own Internet connection

  - Image(s) used:
      - vios-adventerprisek9-m.vmdk.SPA.156-2.T
      - Ubuntu Desktop VM
      - Windows server QEMU VM
      - Webterm docker

          
        
JINJA:
-------------------------------------------------------------------------------------------

Jinja2 is a templating engine that allows you to create dynamic templates 
with placeholders for variables.

When combined with network automation tools like Netmiko Jinja2 helps streamline the 
configuration process for multiple devices.

First, you'll create a Jinja2 template that contains placeholders for the variables 
you want to use.

To define a variable in a Jinja2 template, you use the {{ }} syntax.

Example: 
    interface {{Inteface_name}}
    Description {{Description}}
    ip address {{Address}} {{Netmask}}
    no shut

##Passing Data to the Template##
- When rendering a Jinja2 template, you provide a dictionary or an object containing the 
  data you want to use for variable substitution. 
- The keys in the dictionary correspond to the variable names in the template.
- During template rendering, Jinja2 replaces the variables in the template with their 
  corresponding values from the data dictionary.

The Environment class in Jinja2  manages the template configurations, including:
- template loading:  It knows where to find your templates 
- rendering: It knows how to take your templates and replace the placeholders with the actual values you provide

The FileSystemLoader is a template loader in Jinja2 that loads templates from the file system. 
It searches for templates in a specified directory on the file system and loads them when requested.


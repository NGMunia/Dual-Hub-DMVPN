# Dual-Hub DMVPN Lab with IPsec

DMVPN (Dynamic Multipoint VPN) enables scalable site-to-multiple-site connectivity between a headquarters (HQ) and geographically distributed branch offices. It uses the Internet as the transport network and GRE tunnels as the overlay, allowing dynamic routing between sites. 
When combined with IPsec, DMVPN provides secure, encrypted site-to-site communications.

![DMVPN](https://img.shields.io/badge/DMVPN-Phase2-blue)
![IPsec](https://img.shields.io/badge/IPsec-Secure-red)
![Automation](https://img.shields.io/badge/Automation-Python-green)
![Routing](https://img.shields.io/badge/Routing-EIGRP-orange)

---
![Topology](/Topology.png)

## Why DMVPN?

Most enterprises deploy MPLS or IPsec site-to-site VPNs.  
However, MPLS circuits can be expensive to deploy, especially for a full-mesh topology on multiple regional offices.  
IPsec site-to-site VPNs, on the other hand, are not easily scalable when connecting multiple sites to the headquarters (HQ) or a data center.  

Legacy IPsec VPNs are typically policy-based, meaning interesting traffic is matched against access control lists, which limits flexibility and scalability. In contrast, route-based VPNs using GRE tunnels (DMVPNs) allow routes to be advertised dynamically, enabling more efficient routing between sites.  

DMVPN addresses these limitations with a hub-and-spoke architecture, allowing rapid deployment of spoke connections to the HQ or data center while also providing dynamic full-mesh connectivity between spokes at no additional cost (DMVPN Phase II).  
Additionally, DMVPN allows IPsec to run on top of GRE tunnels, ensuring secure communications between HQ and branch sites and also traffic between branch sites is also secured


## Quick Overview
This lab project demostrates dual-hub DMVPN design with the following:

- **Redundancy:** VRRPv3 with Object tracking
- **Routing:** EIGRP named mode
- **Overlay Security:** IPsec-protected DMVPN tunnels  
- **Automation:** Python-Netmiko
- **Monitoring:** PRTG, SNMP, NetFlow  
- **Services:** Centralized DHCP, DNS,NTP 

---

## Project Objectives

- Implement a dual-hub DMVPN architecture with redundancy  
- Segregate the branch spokes in geographic regions and filter traffic so that regions receive HQ prefixes and prefixes within their regions.
- Secure all tunnels using IPsec cryptography  
- Automate repetitive configurations and device management   
- Deploy centralized network services for branches (namely DHCP, Syslog, SNMP, Netflow) to the server.
- Monitor traffic and device health with SNMP and PRTG  

---

## Lab Architecture

- Dual-hub DMVPN topology connecting multiple branch sites to HQ  
- Each branch has its own Internet connection.  
- Fortigate firewall sits behind the Hub routers to inspect incoming and outgoing traffic
- IPsec secures the DMVPN tunnels end-to-end  
- Centralized Windows server provides:
  - DHCP
  - SNMP, Syslog, Netflow
  - Network monitoring (PRTG) 



---
## Redunndancy:

### VRRPv3:
The Hub architecture is implemented with VRRPv3 as the FHRP on the internet gateway hubs.
VRRP allows multiple gatewy routers to appear as one virtual default gateway to hosts, with one router as the MASTER the other as BACKUP.
VRRPv3 supports both IPv4 and IPv6

*ON ROUTER-1*

```bash
interface Ethernet0/0
 ip address 172.16.255.1 255.255.255.0

 vrrp 10 address-family ipv4
  priority 110
  vrrpv2
  track 1 decrement 60
  address 172.16.255.3 primary
  exit-vrrp
```

*ON ROUTER-2*

```bash
interface Ethernet0/0
 ip address 172.16.255.2 255.255.255.0
 ip nat inside
 ip virtual-reassembly in
 duplex auto
 vrrp 10 address-family ipv4
  address 172.16.255.3 primary
  exit-vrrp
```

### IPSLA and Object tracking:

IPSLA is a feature that allows the router to actively generate traffic to measure perfomance or availability of the network.

With IPSLA the touter detects remote network failure (and switches path depending on the config)

IPSLA works together with object tracking so that if a network tests fail or pass (IPSLA), then an action (Object tracking) will be undetaken.

In the case above, IPSLA/Object-tracking/VRRP are used this way.
 
  -  IPSLA tests the reachability of ISP network (32.19.86.1) through LMR_HQ1 (ICMP pings)
  -  If reachanility fails, Object tracker picks up on this and decrements the VRRP priority on LMR_HQ1 to alower value (by 60) than that of LMR_HQ2
  -  VRRP picks this up and electes LMR_HQ2 as now the master router by the virtual of higher priority number.
  -  Traffic now goes via LMR_HQ1


### Preemption:

When network reachability is restored, LMR_HQ1 advertises a higher priority to LMR_HQ2 (preemption) and it resumes as the Master router.

*IPSLA configuration*

```bash
ip sla 1
 icmp-echo 32.19.86.1 source-interface Ethernet0/3
 frequency 10
ip sla schedule 1 life forever start-time now
```

*Configuring VRRP with Object-tracking*

```bash
track 1 ip sla 1
 delay down 10 up 10


!interface Ethernet0/0
 ip address 172.16.255.1 255.255.255.0
 vrrp 10 address-family ipv4
  priority 110
  vrrpv2
  track 1 decrement 60
  address 172.16.255.3 primary
  exit-vrrp
```

---


## Routing & DMVPN Design (Objective 1)

### mGRE tunnels:

- mGRE tunnel is configured on the hub router as the transport network.
- Spokes are configured with two tunnels one for R1 and the other for R2
- EIGRP is used for internal reachability between HQ and branches  
- **ECMP (Equal-Cost Multi-Path)** utilized to load-share traffic across both DMVPN tunnels  
  
```bash
HUB-ROUTER:

interface Tunnel0
 ip address 192.168.0.1 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip nhrp authentication dmvpnvpn
 ip nhrp network-id 10
 ip nhrp holdtime 300
 ip tcp adjust-mss 1360
 tunnel source Ethernet0/3
 tunnel mode gre multipoint
 tunnel key 10
 tunnel protection ipsec profile crypt-profile


 ```
 ```bash
 SPOKE-ROUTER:

 interface Tunnel0
 ip address 192.168.0.6 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip nhrp authentication dmvpnvpn
 ip nhrp network-id 10
 ip nhrp holdtime 300
 ip nhrp nhs 192.168.0.1 nbma 32.19.86.9 multicast
 ip tcp adjust-mss 1360
 tunnel source Ethernet0/3
 tunnel mode gre multipoint
 tunnel key 10
 tunnel protection ipsec profile crypt-profile shared
!
interface Tunnel1
 ip address 192.168.1.6 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip nhrp authentication dmvpnvpn
 ip nhrp network-id 20
 ip nhrp nhs 192.168.1.1 nbma 32.19.86.10 multicast
 ip tcp adjust-mss 1360
 tunnel source Ethernet0/3
 tunnel mode gre multipoint
 tunnel key 20
 tunnel protection ipsec profile crypt-profile shared
 
 ```

### EIGRP:
EIGRP is used as the overlay routing protocol between the tunnel. 
It is the protocol of choice dur its high convergence in GRE networks.

```bash

router eigrp EIGRP
 !
 address-family ipv4 unicast autonomous-system 100
  !
  af-interface Tunnel1
   bandwidth-percent 25
   no next-hop-self
   no split-horizon
  exit-af-interface
  !
  af-interface Ethernet0/0
   passive-interface
  exit-af-interface
  !
  topology base
  exit-af-topology
  network 172.16.255.0 0.0.0.255
  network 192.168.1.0
 exit-address-family
 exit-address-family
 ```

---
## Route filtering (Objective 2)
EiGRP can use filtering mechanisms to determine which routes are added in its RIB. Distribute lists are used to filter prefixes ingressing the router as shown.
This is done in conjuction with prefix lists:
The snippet below EIGRP filters 192.168.10.0/24, 172.16.2.0/24, 172.16.3.0/24, 172.16.4.0/24 and 172.16.5.0/24 prefixes and allows all other prefixes to be added in the RIB

```bash
outer eigrp EIGRP
 !
 address-family ipv4 unicast autonomous-system 100
  !
  af-interface default
   bandwidth-percent 25
  exit-af-interface
  !
  topology base
   distribute-list prefix EIGRP-filtered-prefixes in 
  exit-af-topology
  network 172.16.1.0 0.0.0.255
  network 192.168.0.0
  network 192.168.1.0
 exit-address-family
!
!
ip prefix-list EIGRP-filtered-prefixes seq 5 deny 172.16.2.0/23 ge 24
ip prefix-list EIGRP-filtered-prefixes seq 10 deny 172.16.4.0/23 ge 24
ip prefix-list EIGRP-filtered-prefixes seq 15 permit 0.0.0.0/0 le 32

```

---

## IPsec & Security (Objective 3)

- All DMVPN tunnels are secured using **IPsec**  
- Ensures confidentiality, integrity, and authentication across the WAN  
- Compatible with dual-hub redundant design  

```bash
crypto isakmp policy 100
 encr aes 192
 hash sha256
 authentication pre-share
 group 14
 lifetime 7200
crypto isakmp key usestrongkey! address 0.0.0.0        
!
!
crypto ipsec transform-set crypt-ts esp-aes 256 esp-sha512-hmac 
 mode transport
!
crypto ipsec profile crypt-profile
 set transform-set crypt-ts 
!
 set transform-set crypto_ts 
!
```

## Automating the Network (Objective 4)
Python uses netmiko libraries to automate network devices.
Netmiko uses SSH as its southbound interface to login to devices and send confguration commands.
Note: SSH must be enabled first for Netmiko to work.

Onboarding a new spoke has been automated to allow for faster deployment of ner branch networks and minimize configuration errors
The script can be seen here:

```bash
/deploying_new_spoke.py
```

Below is a snippet that fetches the start-up configurations of all network devices:

```python
for Devices in chain(
                      HQ_routers.values(), 
                      Region_A.values(), 
                      Region_B.values(), 
                      Region_C.values()
                    ):
    c = ConnectHandler(**Devices)
    c.enable()

    hostname = c.send_command('show version', use_textfsm=True)[0]['hostname']
    output = c.send_command('show startup-config')
    print(output)

```
The above pyton script fetches the start-up configurations of all devices and prints them as output.

### Verifying EIGRP routes:

```python
for devices in chain(
                     HQ_routers.values(),
                     Region_A.values(), 
                     Region_B.values(), 
                     Region_C.values()            
                    ):
  c = ConnectHandler(**devices)
  c.enable()
  hostname = c.send_command('show version', use_textfsm=True)[0]['hostname']
  
  output = c.send_command('show ip route eigrp','\n')
  print(f'\n\n{hostname}\n,{output}')
```
---
## Network Assurance (Objective 5)
SNMP can be configured to send unsolicited traps to notify an NMS of important events such as interface up/down, device reboots, or threshold-based alerts (e.g. high CPU usage).

An NMS (Network Management System) receives these traps and may also poll devices via SNMP to collect performance metrics like CPU and interface utilization, presenting the data in human-readable dashboards and graphs.

Examples of NMS platforms include PRTG and SolarWinds.
Below is a snippet of SNMP configuration

```python

for Devices in chain(
                     HQ_routers.values(), 
                     Region_A.values(), 
                     Region_B.values(), 
                     Region_C.values()      
                    ):
    c = ConnectHandler(**Devices)
    c.enable()

    commands = [
                'ip access-list standard snmp_acl',
                'permit host 172.16.255.254',
                'snmp-server community device_snmp snmp_acl',
                'snmp-server system-shutdown',
                'snmp-server enable traps config',
                'snmp-server host 172.16.255.254 version 2c device_snmp'               
               ]
    print(c.send_config_set(commands))
```

# Centralized Services (Objective 6)

- Each branch site maintains a local Internet connection  
- Windows Server provides:
  - DHCP and DNS for all branches  
  - Network monitoring via **PRTG**  

## Configuring Centralized DHCP (DHCP relay:)

```python

for Devices in chain(
                     Region_A.values(), 
                     Region_B.values(), 
                     Region_C.values()
                    ):
    try:
        c = ConnectHandler(**Devices)
        c.enable()

        hostname = c.send_command('show version', use_textfsm=True)[0]['hostname']

        lan_intf = input(f'What is the LAN interface on {hostname} to be configured with DHCP relay? ')

        commands = [f'interface {lan_intf}',
                    'ip helper-address 172.16.255.254'
                   ]
        print(c.send_config_set(commands),'\n')
        print(f'Router {hostname} has been configured with DHCP relay')
        c.save_config()
        c.disconnect()
    except NetMikoTimeoutException:
        print('Unable to connect. Check if SSH is enabled and the Network device is reachable!! ')
    except Exception as e:
        print(f'Error ,{e}')
        exit()
```
### Monitoring with PRTG:

![Topology](/PRTG.PNG)
---

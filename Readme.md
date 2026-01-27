# Dual-Hub DMVPN Lab with IPsec

**A professional enterprise WAN lab demonstrating advanced DMVPN, IPsec security, EIGRP routing, automation, and network monitoring.**  
Designed to showcase real-world enterprise connectivity, resiliency, and automation practices.

![DMVPN](https://img.shields.io/badge/DMVPN-Phase2-blue)
![IPsec](https://img.shields.io/badge/IPsec-Secure-red)
![Automation](https://img.shields.io/badge/Automation-Python-green)
![EIGRP](https://img.shields.io/badge/EIGRP-ECMP-orange)

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

- **Routing:** EIGRP with ECMP for dual-hub traffic load-sharing 
- **Redisribution** Hub routers redistribute OSPF and EIGRP routess to the mGRE tunnels and fortigate firewall respectively 
- **Overlay Security:** IPsec-protected DMVPN tunnels  
- **Automation:** Python-Netmiko
- **Monitoring:** PRTG, SNMP, NetFlow  
- **Services:** Centralized DHCP, DNS, NTP 
- **Additional security:** The Fortigate firewall allows for management and monitoring traffic to reach the server via firewall policies

---

## Project Objectives

- Implement a dual-hub DMVPN architecture with branch redundancy  
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

## Routing & DMVPN Design

### EIGRP & Load-Sharing

- mGRE tunnel is configured on the hub router as the transport network.
- Spokes are configured with two tunnels one for R1 and the other for R2
- EIGRP is used for internal reachability between HQ and branches  
- **ECMP (Equal-Cost Multi-Path)** utilized to load-share traffic across both DMVPN tunnels  
  
```bash
HUB-ROUTER:

interface Tunnel1
 ip address 172.20.0.1 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip nhrp authentication dmvpnvpn
 ip nhrp network-id 20
 ip tcp adjust-mss 1360
 tunnel source Ethernet0/3
 tunnel mode gre multipoint
 tunnel key 20
 tunnel protection ipsec profile crypt-profile


 ```
 ```bash
 SPOKE-ROUTER:

 interface Tunnel0
 ip address 172.19.0.3 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip nhrp authentication dmvpnvpn
 ip nhrp network-id 10
 ip nhrp holdtime 300
 ip nhrp nhs 172.19.0.1 nbma 72.73.74.9 multicast
 ip tcp adjust-mss 1360
 tunnel source Ethernet0/3
 tunnel mode gre multipoint
 tunnel key 10
 tunnel protection ipsec profile crypt-profile shared
!
interface Tunnel1
 ip address 172.20.0.3 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip nhrp authentication dmvpnvpn
 ip nhrp network-id 20
 ip nhrp nhs 172.20.0.1 nbma 72.73.74.10 multicast
 ip tcp adjust-mss 1360
 tunnel source Ethernet0/3
 tunnel mode gre multipoint
 tunnel key 20
 tunnel protection ipsec profile crypt-profile shared
 
 ```

## EIGRP:
EIGRP is used as the overlay routing protocol between the tunnel. 
It is the protocol of choice dur its high convergence in GRE networks.

```bash

router eigrp EIGRP
 !
 address-family ipv4 unicast autonomous-system 100
  !
  af-interface Tunnel0
   bandwidth-percent 25
   no next-hop-self
   no split-horizon
  exit-af-interface
  !
  topology base
   redistribute ospf 1 metric 100000 1 255 1 1500 route-map OSPF-to-EIGRP-routemap
  exit-af-topology
  network 172.19.0.0 0.0.0.255
 exit-address-family
 ```

## OSPF 
 OSPF is used between the fortigate firewall and hub routers as it supports mult-vendor routing as opposed to EIGRP which is proprietary
 
```bash
On Fortigate Firewall:

 
FortiGate-VM64-KVM # get router info ospf route 
 
OSPF process 0:
Codes: C - connected, D - Discard, O - OSPF, IA - OSPF inter area
       N1 - OSPF NSSA external type 1, N2 - OSPF NSSA external type 2
       E1 - OSPF external type 1, E2 - OSPF external type 2
 
E2 0.0.0.0/0 [1/1] via 10.0.0.6, port5
                   via 10.0.0.2, port4
C  10.0.0.0/30 [1] is directly connected, port4, Area 0.0.0.0
C  10.0.0.4/30 [1] is directly connected, port5, Area 0.0.0.0
C  10.1.20.0/24 [1] is directly connected, port2, Area 0.0.0.0
E2 172.19.0.0/24 [1/20] via 10.0.0.2, port4
E2 172.20.0.0/24 [1/20] via 10.0.0.6, port5
E2 192.168.10.0/24 [1/20] via 10.0.0.6, port5
                          via 10.0.0.2, port4
E2 192.168.20.0/24 [1/20] via 10.0.0.6, port5
                          via 10.0.0.2, port4
E2 192.168.30.0/24 [1/20] via 10.0.0.6, port5
                          via 10.0.0.2, port4
 
 
FortiGate-VM64-KVM #  

```
# Route redistribution:
OSPF and EIGRP routes are redistributed to DMVPN tunnel and Firewall respectively to achieve network reachability:

```bash

ip prefix-list EIGRP-to-OSPF-prefixes seq 5 permit 172.19.0.0/24
ip prefix-list EIGRP-to-OSPF-prefixes seq 10 permit 192.168.10.0/24
ip prefix-list EIGRP-to-OSPF-prefixes seq 15 permit 192.168.20.0/24
ip prefix-list EIGRP-to-OSPF-prefixes seq 20 permit 192.168.30.0/24
!
ip prefix-list OSPF-to-EIGRP-prefixes seq 5 permit 10.1.20.0/24
ip prefix-list OSPF-to-EIGRP-prefixes seq 10 permit 10.1.30.0/24
ipv6 ioam timestamp
!
route-map EIGRP-to-OSPF-routemap permit 10
 match ip address prefix-list EIGRP-to-OSPF-prefixes
!
route-map OSPF-to-EIGRP-routemap permit 10
 match ip address prefix-list OSPF-to-EIGRP-prefixes
!
!
router eigrp EIGRP
 !
 address-family ipv4 unicast autonomous-system 100
  !
  topology base
   redistribute ospf 1 metric 100000 1 255 1 1500 route-map OSPF-to-EIGRP-routemap
  
!
router ospf 1
 router-id 2.2.2.2
 auto-cost reference-bandwidth 100000
 redistribute eigrp 100 subnets route-map EIGRP-to-OSPF-routemap
 default-information originate
!
```


---

## IPsec & Security

- All DMVPN tunnels are secured using **IPsec**  
- Ensures confidentiality, integrity, and authentication across the WAN  
- Compatible with dual-hub redundant design  

```bash
crypto isakmp policy 100
 encr aes 256
 hash sha256
 authentication pre-share
 group 14
 lifetime 7200
crypto isakmp key strongkey address 0.0.0.0        
!
!
crypto ipsec transform-set crypto_ts esp-aes 256 esp-sha256-hmac 
 mode transport
!
crypto ipsec profile crypto_profile
 set transform-set crypto_ts 
!
```

---

## Centralized Services

- Each branch site maintains a local Internet connection  
- Windows Server provides:
  - DHCP and DNS for all branches  
  - Network monitoring via **PRTG**  


![Topology](/PRTG.PNG)
---

# Dual-Hub / Cloud DMVPN Lab with IPsec

**A professional enterprise WAN lab demonstrating advanced DMVPN, IPsec security, EIGRP routing, automation, and network monitoring.**  
Designed to showcase real-world enterprise connectivity, resiliency, and automation practices.

![DMVPN](https://img.shields.io/badge/DMVPN-Phase2-blue)
![IPsec](https://img.shields.io/badge/IPsec-Secure-red)
![Automation](https://img.shields.io/badge/Automation-Python-green)
![EIGRP](https://img.shields.io/badge/EIGRP-ECMP-orange)

---
![Topology](/Topology.png)



## Quick Overview

- **Routing:** EIGRP with ECMP for dual-hub traffic load-sharing  
- **Overlay Security:** IPsec-protected DMVPN tunnels  
- **Automation:** Python-Netmiko
- **Monitoring:** PRTG, SNMP, NetFlow  
- **Services:** Centralized DHCP, DNS, NTP  

---

## Project Objectives

- Implement a dual-hub DMVPN architecture with branch redundancy  
- Secure all tunnels using IPsec cryptography  
- Automate repetitive configurations and device management  
- Configure service resiliency using IPSLA and object tracking  
- Deploy centralized network services for branches  
- Monitor traffic and device health with SNMP and PRTG  

---

## 🗺 Lab Architecture

- Dual-hub DMVPN topology connecting multiple branch sites to HQ  
- Each branch has its own Internet connection for redundancy  
- IPsec secures the DMVPN tunnels end-to-end  
- Centralized Windows server provides:
  - DHCP
  - DNS
  - Network monitoring (PRTG)  



---

## Routing & DMVPN Design

### EIGRP & Load-Sharing

- EIGRP is used for internal reachability between HQ and branches  
- **ECMP (Equal-Cost Multi-Path)** utilized to load-share traffic across both DMVPN tunnels  
- Base NBMA/transport network configuration applied via CLI  
- IPSLA with object tracking on **R1-LAN** ensures preferred default route to Internet via **R1-HUB**  
```bash
HUB-ROUTER:

!
interface Tunnel10
 description DMVPN-1-TUNNEL
 ip address 172.16.0.1 255.255.255.0
 no ip redirects
 ip mtu 1400
 no ip next-hop-self eigrp 100
 no ip split-horizon eigrp 100
 ip nhrp authentication dmvpn1
 ip nhrp map multicast dynamic
 ip nhrp network-id 10
 zone-member security Inside
 ip tcp adjust-mss 1360
 delay 1
 tunnel source GigabitEthernet0/1
 tunnel mode gre multipoint
 tunnel key 10
 tunnel protection ipsec profile crypto_profile
 ```
 ```bash
 SPOKE-ROUTER:
 interface Tunnel10
 description DMVPN-1-TUNNEL
 ip address 172.16.0.2 255.255.255.0
 no ip redirects
 ip mtu 1400
 ip nhrp authentication dmvpn1
 ip nhrp network-id 10
 ip nhrp nhs 172.16.0.1 nbma 32.19.86.2 multicast
 zone-member security Inside
 ip tcp adjust-mss 1360
 delay 1
 tunnel source GigabitEthernet0/1
 tunnel mode gre multipoint
 tunnel key 10
 tunnel protection ipsec profile crypto_profile shared
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

## IPSLA & Object Tracking

- Configured on **R1-LAN** to monitor default route to Internet  
- Ensures **R1-HUB** remains the preferred path  
- Supports high availability for branch connectivity  

```bash
track 1 ip sla 1
 delay down 15 up 15
!
!
ip sla 1
 icmp-echo 32.19.86.1 source-ip 10.1.30.1
 frequency 10
ip sla schedule 1 life forever start-time now
```

---

## Centralized Services

- Each branch site maintains a local Internet connection  
- Windows Server provides:
  - DHCP and DNS for all branches  
  - Network monitoring via **PRTG**  


![Topology](/PRTG.PNG)
---

## 🖥 Lab Images & Platforms

| Component | Image / Platform |
|-----------|----------------|
| Routers | `vios-adventerprisek9-m.vmdk.SPA.156-2.T` |
| Linux VM | Ubuntu Desktop VM |
| Windows Server | Windows Server 2016 QEMU VM |
| PCs / Terminals | Webterm Docker containers |

---

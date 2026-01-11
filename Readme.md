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

---

## IPsec & Security

- All DMVPN tunnels are secured using **IPsec**  
- Ensures confidentiality, integrity, and authentication across the WAN  
- Compatible with dual-hub redundant design  

---

## IPSLA & Object Tracking

- Configured on **R1-LAN** to monitor default route to Internet  
- Ensures **R1-HUB** remains the preferred path  
- Supports high availability for branch connectivity  

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

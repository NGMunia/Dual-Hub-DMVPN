# Dual-Hub DMVPN Lab with IPsec

# Dual-Hub DMVPN with IPsec

This project implements a dual-hub DMVPN Phase II WAN secured with IPsec. The topology simulates an enterprise network with geographically distributed branch offices connected to redundant headquarters hubs using EIGRP.



## Objective of the project:
The objectives of this project are to:

- Build a dual-hub DMVPN WAN
- Secure all tunnel traffic using IPsec
- Provide centralized network services to branch sites
- Monitor the network from a central NOC
- Automate repetitive configuration tasks using Python

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
## Technologies used:

| Technology | Purpose |
|------------|----------|
| Cisco IOS | Routing and Switching |
| DMVPN Phase II | WAN Overlay |
| IPsec | Tunnel Encryption |
| EIGRP Named Mode | Dynamic Routing |
| VRRPv3 | Gateway Redundancy |
| IP SLA | WAN Failure Detection |
| Object Tracking | Automatic Failover |
| Python & Netmiko | Automation |
| SNMP | Device Monitoring |
| NetFlow | Traffic Analysis |
| Syslog | Centralized Logging |
| PRTG | Network Monitoring |
| Windows Server | DHCP, DNS and Monitoring |

---

## Lab Architecture
The topology consists of two headquarters routers operating as redundant DMVPN hubs and multiple branch routers connected over the Internet.

Each branch establishes tunnels to both hubs using mGRE and NHRP. EIGRP provides routing across the overlay while IPsec encrypts all tunnel traffic.



---
# Redunndancy:

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


# Routing 
### DMVPN

Each headquarters router provides an mGRE tunnel for branch connectivity.

Branch routers establish tunnels to both hubs, providing redundancy and allowing Equal-Cost Multi-Path (ECMP) forwarding when both paths are available.
  
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

### EIGRP:
EIGRP Named Mode is used as the overlay routing protocol between headquarters and branch sites.

The routing design provides:

- Automatic route exchange
- Fast convergence
- Equal-cost load balancing
- Dynamic route advertisement

---
# Route filtering Route Filtering

Regional branches should only learn headquarters routes and routes within their own region.

Prefix Lists together with EIGRP distribute-lists are used to control route advertisement and reduce unnecessary entries in the routing table.

This approach improves scalability while keeping routing tables smaller on branch routers.

---

# Security

All DMVPN tunnels are protected using IPsec in transport mode.

IPsec provides:

- Encryption
- Integrity checking
- Peer authentication

This ensures traffic remains protected between headquarters and branch offices, including spoke-to-spoke communication.
---

# Automation

Python and Netmiko are used to automate repetitive administrative tasks.

Automation scripts included in this repository perform tasks such as:

- Deploying new branch routers
- backing up startup configurations
- Verifying configurations

Example:- 
```python
output = c.send_command("show startup-config")
```
---

# Network Monitoring

The network is monitored centrally using PRTG.

Routers export operational information through:

- SNMP
- NetFlow
- Syslog

This allows administrators to monitor:

- Device availability
- CPU utilization
- Memory usage
- Interface bandwidth
- Traffic flows
- Network events

Centralized monitoring provides a single view of the network, making it easier to detect outages and troubleshoot problems.

### Monitoring with PRTG:

![Topology](/PRTG.PNG)
---

# Verification

The following commands were used to validate the deployment.
```bash
show dmvpn

show ip nhrp

show ip route eigrp

show ip eigrp neighbors

show crypto isakmp sa

show crypto ipsec sa

show standby

show track
```

## steps to setup bgp between 2 neighbors

in this example we are establishing a bgp neighborship between leaf01 and leaf02

### leaf01 config

#### Before
1. move to `vtysh` mode and check bgp config
```
admin@leaf01:~$ vtysh

Hello, this is FRRouting (version 7.5.1-sonic).
Copyright 1996-2005 Kunihiro Ishiguro, et al.

leaf01# show ip bgp summary
% BGP instance not found

```
#### Configure
2. move to `config` mode and  setup a router-id
```
leaf01# configure
leaf01(config)# router-id 1.1.1.1
leaf01(config)#
```
3. create a bgp process with an autonomous system number `65121`
```
leaf01(config)# router bgp 65121
leaf01(config-router)# neighbor 12.12.12.13 remote-as 65122
leaf01(config-router)#
```

#### After

4. check bgp summary
```
leaf01# show ip bgp summary

IPv4 Unicast Summary:BGP router identifier 1.1.1.1, local AS number 65121 vrf-id 0
BGP table version 0
RIB entries 0, using 0 bytes of memory
Peers 1, using 21 KiB of memory

Neighbor        V         AS   MsgRcvd   MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd   PfxSnt
12.12.12.13     4      65122         0         0        0    0    0    never       Active        0

Total number of neighbors 1
```
> Note that all the counters are zeros because we haven't configure the other side at this point

### leaf02 config

#### Before
1. same as `leaf01`

### Configure
2. setup router-id for `leaf02`
```
leaf02# config
leaf02(config)# router-id 2.2.2.2
leaf02(config)#
```

3. configure bgp process and neighborship 
(make sure that neighbor IP and ASN match what we configured for leaf01)
```
leaf02(config)# router bgp 65122
leaf02(config-router)# neighbor 12.12.12.12 remote-as 65121
leaf02(config-router)#

```
#### After

4. check bgp summary
```
leaf02# show bgp summary

IPv4 Unicast Summary:
BGP router identifier 2.2.2.2, local AS number 65122 vrf-id 0
BGP table version 0
RIB entries 0, using 0 bytes of memory
Peers 1, using 21 KiB of memory

Neighbor        V         AS   MsgRcvd   MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd   PfxSnt
12.12.12.12     4      65121         4         4        0    0    0 00:01:33     (Policy) (Policy)

Total number of neighbors 1

```
> Note that neighborship has been established and bgp messages are being exchanged








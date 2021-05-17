## Steps to configure interface

### Before

1. move to the vtysh mode
```
admin@leaf01:~$ vtysh

Hello, this is FRRouting (version 7.5.1-sonic).
Copyright 1996-2005 Kunihiro Ishiguro, et al.

leaf01#
```
2. check current config

```
leaf01# show interface brief

Interface       Status  VRF             Addresses
---------       ------  ---             ---------
Bridge          up      default
Ethernet0       up      default
Ethernet4       up      default
Ethernet8       up      default
Ethernet12      up      default
Ethernet16      up      default
Ethernet20      up      default         172.0.1.1/31
Ethernet24      up      default         172.0.2.1/31
Ethernet28      up      default         172.0.3.1/31
Ethernet32      up      default         172.0.4.1/31
Ethernet36      up      default
Ethernet40      up      default
Ethernet44      up      default
Ethernet48      up      default
```
### configuration

3. move to config mode and setup the ip address for `Ethernet12`
```
leaf01# configure terminal
leaf01(config)# interface Ethernet12
leaf01(config-if)# ip address 12.12.12.12/31
leaf01(config-if)# no shutdown
leaf01(config-if)#

```
### After

4. check results
```
leaf01# show interface brief

Interface       Status  VRF             Addresses
---------       ------  ---             ---------
Bridge          up      default
Ethernet0       up      default
Ethernet4       up      default
Ethernet8       up      default
Ethernet12      up      default         12.12.12.12/31
Ethernet16      up      default
Ethernet20      up      default         172.0.1.1/31
Ethernet24      up      default         172.0.2.1/31
Ethernet28      up      default         172.0.3.1/31
Ethernet32      up      default         172.0.4.1/31
Ethernet36      up      default
Ethernet40      up      default
Ethernet44      up      default
Ethernet48      up      default
```

### SUMMARY

in this scenario a VLAN missconfiguration was introduced which drops packets to and from all ip addresses within `VLAN 20`

#### HOW?
this is acheived by configuring the trunk port on `sw1` to allow only `VLAN 10`.

from [sw1.conf](./sw1.conf)

```
!
interface GigabitEthernet0/0
 switchport trunk encapsulation dot1q
 switchport trunk allowed vlan 10
 switchport mode trunk
 media-type rj45
 duplex full
 no negotiation auto
!

```

#### SYMPTOMS

- traffic within the same `VLAN 20` (doesn't need L3 routing) works as usual.
- inter-vlan traffic needs routing to reach the final destination, and since `VLAN 20` is not on the allowed vlans list on `sw1` the router `SH1`(which is the default gateway for hosts in `VLAN 20`) will not be able to reach any hosts in that VLAN.

##### EXAMPLES
we can see this illustrated in the following examples

1. refrence test, `pc146` can reach `pc02` because `pc02` in in `VLAN 10` which is on the allowed list
```
PC164> ping 10.11.200.02
84 bytes from 10.11.200.2 icmp_seq=1 ttl=62 time=5.714 ms
84 bytes from 10.11.200.2 icmp_seq=2 ttl=62 time=2.707 ms
84 bytes from 10.11.200.2 icmp_seq=3 ttl=62 time=3.730 ms
84 bytes from 10.11.200.2 icmp_seq=4 ttl=62 time=3.282 ms
84 bytes from 10.11.200.2 icmp_seq=5 ttl=62 time=2.582 ms
```

2. the same `pc146` gets a `timeout` when trying to reach `pc34` as its packets are dropped at `sw1-e0` interface
```
PC164> ping 10.11.200.34
10.11.200.34 icmp_seq=1 timeout
10.11.200.34 icmp_seq=2 timeout
10.11.200.34 icmp_seq=3 timeout
10.11.200.34 icmp_seq=4 timeout
10.11.200.34 icmp_seq=5 timeout
```

3. `pc34` cannot even reach its default gateway `10.11.200.33` (SH1) as its packets are dropped as `sw1-e0` interface
```
PC34> ping 10.11.200.02
host (10.11.200.33) not reachable
```

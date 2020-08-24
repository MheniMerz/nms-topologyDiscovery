import os
from logger import log
import json
import re
import pprint
import copy
from constants import *
from datetime import datetime


class NetworkTopology:
    # this is the primary dictionary that will become graph.json

    def __init__(self):
        self.visualization_dict = {'nodes': [], 'links': []}
        self.interfaces_dict = dict()
        self.neighborships = dict()
        log("Initializing NetworkTopology class")
        # Load Interface Stats if exist previously
        try:
            with open('results/interface_stats.json') as json_file:
                self.interface_stats = json.load(json_file)
        except FileNotFoundError:
            log("File doesn't exists, creating...")
            self.interface_stats = dict()

    def classifyDeviceHostnameToGroup(self, s_device_name):
        # categorize devices and define corresponding image
        log("Hostname matched[key]: " + s_device_name)
        group = "1"  # for key (source hostname)
        image = "default.png"
        for node_pattern in NODE_HIERARCHY:
            log("Pattern: " + node_pattern[0])
            pattern = re.compile(node_pattern[0])
            if pattern.match(s_device_name):
                log("match")
                group = node_pattern[1]
                image = node_pattern[2]
                break
        log("Final GROUP for key: " + s_device_name + " is " + group)
        return (group,image)

    def addDevice(self, s_device_name):
        if not self.isDeviceDefined(s_device_name):
            group_number, image_name = self.classifyDeviceHostnameToGroup(s_device_name)
            self.visualization_dict['nodes'].append({"id": s_device_name, "group": group_number, "image": image_name})
            self.interfaces_dict[s_device_name] = []
            self.neighborships[s_device_name] = []
            return True
        else:
            return False

    def isDeviceDefined(self,s_device_name):
        log("isDeviceDefined: " + s_device_name)
        for node in self.visualization_dict['nodes']:
            log(str(node['id'] + " == " + s_device_name))
            if node['id'] == s_device_name:
                log("MATCH!")
                return True
        return False

    def getLinkSpeedFromName(self, interface_name):
        log("Interface matched: " + interface_name)
        speed = "1"  # DEFAULT
        for speed_pattern in LINK_SPEEDS:
            log("Pattern: " + speed_pattern[0])
            pattern = re.compile(speed_pattern[0])

            if pattern.match(interface_name):
                speed = speed_pattern[1]
                log('match!')

        log("Final SPEED:" + speed)
        return speed

    def getDeviceInterfaceUtilizations(self,deviceid,interface_name):
        if deviceid not in self.interface_stats:
            log("device not in STATS! to getDeviceInterfaceUtilizations")
            return 0

        for interface in self.interface_stats[deviceid]['interfaces']:
            if interface['ifDescr'] == interface_name:
                if 'utilization' in interface:
                    return interface['utilization']
                else:
                    return 0

    def addLink(self, node_a, node_b, value, a_local_int_index, a_local_int_name, b_local_int_name):

        # Get the highest utilization for this pair
        a_utilization = self.getDeviceInterfaceUtilizations(node_a, a_local_int_name)
        b_utilization = self.getDeviceInterfaceUtilizations(node_b,b_local_int_name)
        if a_utilization is None:
            a_utilization = 0
        if b_utilization is None:
            b_utilization = 0

        highest_utilization = max(a_utilization,b_utilization)

        # check if these two nodes are already connected with such value link
        for link in self.visualization_dict['links']:
            if link['source'] == node_a and link['target'] == node_b:
                log("Link between " + node_a + " and " + node_b + " already exists")
                if link['highest_utilization'] < highest_utilization:
                    log("But has lower utilization, so adding the new on there")
                    link['highest_utilization'] = highest_utilization
                return False
            if link['source'] == node_b and link['target'] == node_a:
                log("Link between " + node_b + " and " + node_a + " already exists, but adding new target_interfaces")
                link["target_interfaces"].append(a_local_int_name)
                link["target_interfaces_indes"].append(a_local_int_index)
                if link['highest_utilization'] < highest_utilization:
                    log("But has lower utilization, so adding the new on there")
                    link['highest_utilization'] = highest_utilization
                return False
            if str(node_a) == str(node_b):
                log("Link between " + node_b + " and " + node_a + " not allowed as the same source/target")
                return False

        # Paranoid check if we are maybe adding link for a device that was not in the device/nodes list, so we add it
        if not self.isDeviceDefined(node_a):
            self.addDevice(node_a)
        if not self.isDeviceDefined(node_b):
            self.addDevice(node_b)

        # Now we update the dictionary
        self.visualization_dict['links'].append({"source": node_a,
                                                 "target": node_b,
                                                 "speed": value,
                                                 "highest_utilization": highest_utilization,
                                                 "source_interfaces": [a_local_int_name],
                                                 "source_interfaces_indes": [a_local_int_index],
                                                 "target_interfaces": [],
                                                 "target_interfaces_indes": []
                                                 })  #TODO change highest_utilization for real usage
        return True

    def dumpToJSON(self):
        # this will dump all the needed files for visualization
        os.makedirs('results', exist_ok=True)
        with open('results/graph.json', 'w') as outfile:
            json.dump(self.visualization_dict, outfile, sort_keys=True, indent=4)
            log("JSON printed into graph.json")

        with open('results/interfaces.json', 'w') as outfile:
            json.dump(self.interfaces_dict, outfile, sort_keys=True, indent=4)
            log("JSON printed into interfaces.json")



    def getDeviceInterface(self, s_device_name, interface_index):
        for interface in self.interfaces_dict[s_device_name]:
            if interface['index'] == interface_index:
                return interface

        return

    def getDeviceInterfaceIndex(self, s_device_name, interface_name):
        for interface in self.interfaces_dict[s_device_name]:
            if str(interface['ifDescr']) == str(interface_name):
                return interface['index']

        return


    def addNeighborships(self, local_device_name, local_int_index, local_interface_name, neighbor_name, neighbor_interface_name ):

        # DOUBLE ENTRY PROTECTION
        for neighbor in self.neighborships[local_device_name]:
            if neighbor['local_int_index'] == local_int_index and neighbor['local_intf'] == local_interface_name and neighbor['neighbor'] == neighbor_name and neighbor['neighbor_intf'] == neighbor_interface_name:
                log("This neighborship exists already, skipping..")
                return False


        local_interface = self.getDeviceInterface(local_device_name, local_int_index)
        if local_interface == None:
            log("Error, could not get local_interface based on index: " + str(local_int_index) + " on host " + local_device_name)
            alternative_index = self.getDeviceInterfaceIndex(local_device_name,local_interface_name)
            log("USING Alternative INDEX since LLDP lldpLocPortId is different than IF-MIBs: " + str(alternative_index))
            local_int_index = alternative_index

        log(str("Interface: " + local_interface_name))
        neighborship = {'local_int_index': local_int_index,
                        'local_intf': local_interface_name,
                        'neighbor': neighbor_name,
                        'neighbor_intf': neighbor_interface_name}

        self.neighborships[local_device_name].append(neighborship)


    def generateNoNeighborsInterfacesDict(self):

        #Create empty dir
        no_neighbor_interfaces = dict()

        # go via devices of interfaces dict
        for device_a in self.interfaces_dict:

            # add device to new dict as key and empty array for no neighbor devices
            no_neighbor_interfaces[device_a] = []

            # iterate over this device interfaces
            for interface_a in self.interfaces_dict[device_a]:

                # This controls if this interface should be added
                bool_interface_without_neighbor = True

                # now go via the LLDP neighborship dict
                for device_b in self.neighborships:

                    # only if the source neighbor is the same device
                    if device_b == device_a:

                        # iterate over neighborships of this device
                        # iterate over neighborships of this device
                        for neighborship_of_device_a in self.neighborships[device_b]:

                            # We found a neighborship on the device_a interface via index comparison
                            if neighborship_of_device_a['local_int_index'] == interface_a['index']:

                                # Mark that this interface should not be added
                                bool_interface_without_neighbor = False

                if bool_interface_without_neighbor:
                    no_neighbor_interfaces[device_a].append(interface_a)

        # Generate cleaned dictionary
        return no_neighbor_interfaces



    def addDeviceInterface(self,
                           s_device_name, 
                           interface_index_in_IFMIB,
                           ifDescr, 
                           ifType, 
                           ifMtu, 
                           ifSpeed, 
                           ifPhysAddress,
                           ifAdminStatus,
                           ifOperStatus
                           ):
        for ignored_iftype in IGNORED_IFTYPES:
            if ignored_iftype == str(ifType):
                log("This interface is of INGORED_IFTYPE and will be skipped:" + ignored_iftype)
                return

        ###
        # Here we are connected, let collect Interfaces
        ###
        interface_dict = {
            'index': interface_index_in_IFMIB,
            'ifDescr': ifDescr,
            'ifType': ifType,
            'ifMtu': ifMtu,
            'ifSpeed': ifSpeed,
            'ifPhysAddress': ifPhysAddress,
            'ifAdminStatus': ifAdminStatus,
            'ifOperStatus': ifOperStatus
        }
        self.interfaces_dict[s_device_name].append(interface_dict)






# Test operation to create JSON from model
if __name__ == "__main__":
    nodes = []
    candidate = {"id": "deviceA", "group": "1"}
    nodes.append(candidate)
    candidate = {"id": "deviceB", "group": "2"}
    nodes.append(candidate)

    links = []
    links.append({"source": "deviceA", "target": "deviceB", "value": "10"})

    visualization_dict = {'nodes': nodes, 'links': links}
    with open('graph.json', 'w') as outfile:
        json.dump(visualization_dict, outfile, sort_keys=True, indent=4)
        log("")
        log("JSON printed into graph.json")


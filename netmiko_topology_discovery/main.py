import netmiko
import configparser
import json
from types import SimpleNamespace
import concurrent.futures
from ntc_templates.parse import parse_output
from models.node import Node
import models.interface
from models.interface import Interface
from models.link import Link

def run_cmd(ip, dev_type, username, password, command):
    # create connection
    connection = netmiko.ConnectHandler(
            ip=ip,
            device_type=dev_type,
            username=username,
            password=password,
    )
    # run the first command to get the interfaces on the current node
    result = connection.send_command(command)
    # use ntc_templates to parse the output into json
    parsed_result = parse_output(
            platform = dev_type,
            command = command,
            data = result
            )
    # beutify the json file and print
    parsed_result = json.dumps(parsed_result, indent=2)
    connection.disconnect()
    return parsed_result 


def get_nodes():
    return_value = ""
    threads = list()
    for device in json.loads(config['TARGETS']['devices']):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(
                    run_cmd,
                    device,
                    "cisco_ios",
                    config['AUTH']['username'],
                    config['AUTH']['password'],
                    "show lldp neighbors detail"
            )
            return_value = future.result()
        neighbors = json.loads(return_value, object_hook=lambda d: SimpleNamespace(**d))
        for i in neighbors:
            nb = i.neighbor.split(".")[0].lower() 
            if nb not in nodes:
                nodes[nb] = Node(
                        i.neighbor, 
                        i.chassis_id, 
                        i.management_ip, 
                        i.capabilities)
            if i.local_interface != "" and i.neighbor_interface != "":
                links[device+"<->"+nb]= Link(
                        [Interface(i.local_interface,"","","","",device),
                        Interface(i.neighbor_interface,"","","","",nb)]
                        )                

def get_interfaces():
    threads = list()
    for device in json.loads(config['TARGETS']['devices']):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(
                    run_cmd,
                    device,
                    "cisco_ios",
                    config['AUTH']['username'],
                    config['AUTH']['password'],
                    "show interface"
                    )
            return_value = future.result()
        ints = json.loads(return_value, object_hook=lambda d: SimpleNamespace(**d))
        for i in ints:
            nodes[device].add_interface(Interface(
                i.interface,
                i.link_status,
                i.protocol_status,
                i.ip_address,
                i.address,
                device
                ))
        set_vlan_for_interface(nodes[device])

def set_vlan_for_interface(device):
    if device.is_switch():
        dev_name = device.name_from_fqdn()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(
                    run_cmd,
                    dev_name,
                    "cisco_ios",
                    config['AUTH']['username'],
                    config['AUTH']['password'],
                    "show interfaces switchport"
                    )
            return_value = future.result()
            ports= json.loads(return_value, object_hook=lambda d: SimpleNamespace(**d))
            for p in ports:
                tmp = models.interface.normalize_interface(p.interface)
                nodes[dev_name].interfaces[tmp].assign_access_vlan(p.access_vlan)
                nodes[dev_name].interfaces[tmp].assign_native_vlan(p.native_vlan)

# open config file
config = configparser.ConfigParser()
config.read('config.ini')
config.sections()


# global variables that hold the results
nodes = {}
links = {}
#graph = Graph(nodes, links)

# check config file for mandatory sections
if 'TARGETS' not in config or 'AUTH' not in config:
    log('Syntax error in configuration file. Please provide AUTH and TARGETS')
    log('ERROR: failed to load the configuration file')
    log('Exiting')
    exit(1)

get_nodes()
get_interfaces()

#for l in links:
#    print(l +":"+links[l].to_string())

for n in nodes:
    print(n +":"+nodes[n].to_string())


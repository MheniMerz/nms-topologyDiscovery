import pprint
import argparse
import textwrap
import json
import configparser
import snmprequests
from pysnmp import hlapi
from logger import log
from topologyModel import NetworkTopology
from constants import *
import time

def get_topology(args):
    log("##### physical topology service #####")
    
    # create the data model of the topology
    topology_model = NetworkTopology()
    
    # open config file
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    
    # check config file for mandatory sections
    if 'TARGETS' not in config or 'AUTHENTICATION' not in config:
        log('Syntax error in configuration file')
        log('ERROR: failed to load the configuration file')
        log('Exiting')
        exit(1)
    
    # loop on devices given in config file
    for device in json.loads(config['TARGETS']['devices']):
        device = device.replace('\n', '')
        print("############################################")
        print(f'Testing access to {device} ...\n')
        log("Testing access to " + device)
        log("  Retreiving Hostname ")

        try:
            snmpHostname = snmprequests.get(device, sysName_named_oid,
                                          hlapi.CommunityData(config['AUTHENTICATION']['snmpCommunityString']))
            log(' = '.join([x.prettyPrint() for x in snmpHostname]))
            log(" numeric OID: " + str(tuple(snmpHostname[0][0])))
            log(" hostname: " + str(snmpHostname[0][1]))
        except RuntimeError as e:
            log("Runtime Error: " + str(e))
            continue
        except (ValueError, TypeError):
            log("Error " + str(TypeError))
            continue

        log("Retreiving Hostname done!")
    
        # GET INTERFACES TABLE
        try:
            log("Retreiving Interfaces")
            log("  INTERFACES TABLE: ")
            rawInterfacesTable = snmprequests.get_table(device, interfaces_table_named_oid,
                                                     hlapi.CommunityData(config['AUTHENTICATION']['SnmpCommunityString']))
            for row in rawInterfacesTable:
                for item in row:
                    log(' = '.join([x.prettyPrint() for x in item]))
                log('')

        except RuntimeError as e:
            log("  Runtime Error: " + str(e))
            continue
        except (ValueError, TypeError):
            log("  Error " + str(TypeError))
            continue
        
        log("Retreiving Interfaces done!")

        # GET LLDP TABLE
        try:
            log("Retreiving LLDP neighbors table")
            log("LLDP TABLE: ")
            
            rawTable = snmprequests.get_table(device, lldp_table_named_oid,
                                           hlapi.CommunityData(config['AUTHENTICATION']['SnmpCommunityString']))
            for row in rawTable:
                for item in row:
                    log(' = '.join([x.prettyPrint() for x in item]))
                log('')

        except RuntimeError as e:
            log("Runtime Error: " + str(e))
            continue
        except (ValueError, TypeError):
            log("Error " + str(TypeError))
            continue

        # Populate the data model 
        topology_model.addDevice(str(snmpHostname[0][1]))

        # device interfaces
        for row in rawInterfacesTable:
            # index number from OID
            oid = tuple(row[0][0])
            topology_model.addDeviceInterface(str(snmpHostname[0][1]),  # deviceid
                                              oid[-1],  # INDEX
                                              str(row[0][1]),  # ifDescr
                                              str(row[1][1]),  # ifType
                                              str(row[2][1]),  # ifMtu
                                              str(row[3][1]),  # ifSpeed
                                              str(row[4][1].prettyPrint()),  # ifPhysAddress
                                              str(row[5][1]),  # ifAdminStats
                                              str(row[6][1]))  # ifOperStatus


        # LLDP links
        for row in rawTable:
            # Add neighborships
            oid = tuple(row[0][0])
            local_in_index = oid[-2]
            # Get interface name via LLDP local int table
            local_interface_name = snmprequests.get(device, [('LLDP-MIB', 'lldpLocPortId', local_in_index)],
                                                 hlapi.CommunityData(config['AUTHENTICATION']['SnmpCommunityString']))
            # Repairing H3Cs bad indexes by searching for index via name
            local_in_index = topology_model.getDeviceInterfaceIndex(str(snmpHostname[0][1]), str(local_interface_name[0][1]))
            
            log("Local_interface_name: " + str(local_interface_name[0][1]))
            log(' = '.join([x.prettyPrint() for x in local_interface_name]))
            # Add links
            topology_model.addLink(str(snmpHostname[0][1]),  # node_a
                                   str(row[0][1]),  # node_b
                                   topology_model.getLinkSpeedFromName(str(row[2][1])),
                                   local_in_index,  # a_local_int_index
                                   str(local_interface_name[0][1]),  # a_local_int_name
                                   str(row[2][1])  # lldpRemPortId
                                   )
            log("Localintindex : " + str(local_in_index))
            topology_model.addNeighborships(str(snmpHostname[0][1]),
                                            local_in_index,
                                            str(local_interface_name[0][1]),
                                            str(row[0][1]),
                                            str(row[2][1]))

    # create JSON file
    topology_model.dumpToJSON()
    del topology_model


    return "DONE!"

#if __name__ == "__main__":
def run():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("-R", "--REPEAT", default=0, type=int)
    parser.set_defaults(func=get_topology)

    # Binding parsers to arges
    args = parser.parse_args()
    if args.REPEAT == 0:
        return_code = args.func(args)
    else:
        while (True):
            return_code = args.func(args)
            time.sleep(args.REPEAT)

    print("return code:" + str(return_code))
    exit(return_code)


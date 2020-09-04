from pysnmp import hlapi
import code
import itertools

# for other SNMP versions visit the documentation
# http://snmplabs.com/pysnmp/examples/hlapi/asyncore/sync/manager/cmdgen/snmp-versions.html


def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_object_types_from_named_oid(oids)
    )
    return fetch(handler)

def get_table(target, oids, credentials, start_from=0, port=161,
              engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.nextCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_object_types_from_named_oid(oids),
        lexicographicMode=False
    )
    return array_to_table(fetch(handler),len(oids))


def fetch(handler):
    result = []

    for (errorIndication,
         errorStatus,
         errorIndex,
         varBinds) in handler:

        if errorIndication:
            print(errorIndication)
            raise RuntimeError('Got SNMP error: {0}'.format(errorIndication))
        elif errorStatus:
            print('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
            raise RuntimeError('Got SNMP error: {0}'.format(errorStatus))
        else:
            for varBind in varBinds:
                result.append(varBind)

    print("DEBUG: len of result from fetch() " + str(len(result)) )
    return result

def construct_object_types_from_named_oid(list_of_oid_name_tuplets):
    object_types = []
    for oid in list_of_oid_name_tuplets:
        addr = []
        for x in oid:
            addr.append(x)
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(*addr).addMibSource('.')))
    return object_types

def array_to_table(data,collumns):
    result = []
    row = []
    collumn_index = 0
    for x in data:
        if collumn_index == 0:
            row.append(x)
            collumn_index = 1
        elif collumn_index < collumns:
            collumn_index = collumn_index + 1
            row.append(x)
            if collumn_index == collumns:
                result.append(row)
        else:
            collumn_index = 1
            row = [x] #starts new row

    return result



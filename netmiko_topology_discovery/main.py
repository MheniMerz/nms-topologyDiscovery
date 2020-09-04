import netmiko
import configparser
import json
import threading
from ntc_templates.parse import parse_output

def run_cmd(ip, dev_type, username, password, command):
    # create connection
    connection = netmiko.ConnectHandler(
            ip=ip,
            device_type=dev_type,
            username=username,
            password=password,
    )
    # run the command on the target device
    result = connection.send_command(command)
    # use ntc_templates to parse the output into json
    parsed_result = parse_output(
            platform=dev_type,
            command=command,
            data=result
            )
    # beutify the json file and print
    parsed_result = json.dumps(parsed_result, indent=2)
    print(parsed_result)
    connection.disconnect()
    return parsed_result


# open config file
config = configparser.ConfigParser()
config.read('config.ini')
config.sections()

# check config file for mandatory sections
if 'TARGETS' not in config or 'AUTH' not in config:
    log('Syntax error in configuration file')
    log('ERROR: failed to load the configuration file')
    log('Exiting')
    exit(1)

threads = list()
for device in json.loads(config['TARGETS']['devices']):
    th = threading.Thread(
            target=run_cmd, 
            args=(
                device,
                "cisco_ios",
                config['AUTH']['username'],
                config['AUTH']['password'], 
                "show lldp neighbors"
        ))
    threads.append(th)

# starting the threads
for th in threads:
    th.start()

# waiting for the threads to finish
for th in threads:
    # get return value from the thread
    th.join()
    

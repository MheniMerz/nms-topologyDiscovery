import os
import datetime
import configparser
from constants import *


def log(string, severity=3):
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()
    os.makedirs('logs', exist_ok=True)
    outfile = open(config['LOGGING']['logFile'], "w+")
    timestamp = datetime.datetime.now().strftime("%Y %b %d-%H:%M:%S")
    outfile.write(timestamp + ": " + string + "\n")
    outfile.close()

    if config['LOGGING']['debug'] == "yes":
        print(timestamp + ": " + string)


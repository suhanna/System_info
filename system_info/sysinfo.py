#!/usr/bin/python3

import os
import platform
import socket as sk
import sys

import cpuinfo
import math
import psutil
import shutil
import subprocess

RAM_Types = {
    0 : "DDR4",
    1 : "Other",
    2 : "DRAM",
    3 : "Synchronous DRAM",
    4 : "Cache DRAM",
    5 : "EDO",
    6 : "EDRAM",
    7 : "VRAM",
    8 : "SRAM",
    9 : "RAM",
    10 : "ROM",
    11 : "Flash",
    12 : "EEPROM",
    13 : "FEPROM",
    14 : "EPROM",
    15 : "CDRAM",
    16 : "3DRAM",
    17 : "SDRAM",
    18 : "SGRAM",
    19 : "RDRAM",
    20 : "DDR",
    21 : "DDR2",
    22 : "DDR2 FB-DIMM",
    24 : "DDR3",
    25 : "FBD2",
}

class SystemInfo(object):
    """ System Information"""
    def __init__(self):
        self.title = "System Management"

    def platformName(self):
        return platform.system()

    def systemSpec(self):
        """ Collect Hardware details for Linux, Windows and Mac """

        cinfo = cpuinfo.get_cpu_info()
        data = {}
        data["Processor"] = cinfo['brand_raw']
        data["CPU"] = cinfo['count']

        if os_info.platformName() == 'Linux':
            Hardware_info = self.getUnixSystemSpec(data)
        elif os_info.platformName() == 'Windows':
            Hardware_info = self.getWindowsSystemSpec(data)
        elif os_info.platformName() == 'Darwin':
            Hardware_info = self.getMacSystemSpec(data)
        else:
            print("Operating system is not detected.")
            sys.exit(0)

        return Hardware_info

    def getUnixSystemSpec(self, data):
        """ Collect hardware info for Linux """

        data["Total Disk Space"] = str(shutil.disk_usage("/")[0] // (2**30))+"GB"
        data["Available Space"] = str(shutil.disk_usage("/")[2] // (2**30))+"GB"
        try:
            data["Host Name"] = subprocess.check_output("hostname", stderr=open(os.devnull, 'w'), shell=True).decode('utf-8').strip("\n")
        except Exception as error:
            data["Host Name"] = None
        try:
            data["Ip"] = subprocess.check_output("ip route get 1",stderr=open(os.devnull, 'w'), shell=True).decode('utf-8').split('src ')[1].split(' ')[0]
        except Exception as error:
            data["Ip"] = None
        try:
            data["Operating System"] = str(subprocess.check_output("cat /etc/*-release | grep NAME=",stderr=open(os.devnull, 'w'), shell=True)).partition("\\nNAME=")[2].split("\\n")[0].strip('"')
        except Exception as error:
            data["Operating System"] = None
        try:
            data["OS Version"] = str(subprocess.check_output("cat /etc/*-release | grep VERSION_ID",stderr=open(os.devnull, 'w'), shell=True)).partition('VERSION_ID=')[2].strip('"')[:-4]
        except Exception as error:
            data["OS Version"] = None
        try:
            data["CPU_Core"] = str(subprocess.check_output('lscpu | grep socket:', stderr=open(os.devnull, 'w'), shell=True)).split(':')[1].strip(' ').strip("\\n'")
        except Exception as error:
            data["CPU_Core"] = None
        try:
            data["HD Size"] = str(subprocess.check_output('sudo lshw -class disk | grep size', stderr=open(os.devnull, 'w'), shell=True)).split('(',1)[1].split(')')[0]
        except Exception as error:
            data["HD Size"] = None
        try:
            data["Manufacturer"] = str(subprocess.check_output('sudo dmidecode -s system-manufacturer', stderr=open(os.devnull, 'w'), shell=True))[2:-3]
        except Exception as error:
            data["Manufacturer"] = None
        try:
            data["Model"] = str(subprocess.check_output('sudo dmidecode -s system-product-name', stderr=open(os.devnull, 'w'), shell=True))[2:-3]
        except Exception as error:
            data["Model"] = None
        try:
            data["Ram_Type"] = subprocess.check_output('sudo dmidecode --type 17 | grep -B 2 "Type Detail: Synchronous" | grep -w "Type:"', stderr=open(os.devnull, 'w'), shell=True).decode('utf-8').split('\tType:')[1].strip(' ').strip('\n')
        except Exception as error:
            data["Ram_Type"] = None
        try:
            ramSize = round(int(subprocess.check_output("grep MemTotal /proc/meminfo",stderr=open(os.devnull, 'w'), shell=True).decode('utf-8').split()[1])/1024000)
            data["Ram_Size"] = str(ramSize) + " GB"
        except Exception as error:
            data["Ram_Size"] = None
        try:
            data["HD_Type"] = str(subprocess.check_output('sudo lshw -class disk -class storage | grep description', stderr=open(os.devnull, 'w'),shell=True)).split('\\n')[0].split(':')[1].strip(' ')
        except Exception as error:
            data["HD_Type"] = None
        try:
            data["Serial_Number"] = str(subprocess.check_output('sudo dmidecode -s system-serial-number', stderr=open(os.devnull, 'w'), shell=True))[2:-3]
        except Exception as error:
            data["Serial_Number"] = None

        return data

    def getWindowsSystemSpec(self, data):
        """ Collect hardware info for Windows """

        data["Ip"] = sk.gethostbyname(sk.gethostname())
        data["OS Version"] = platform.version()
        partitions = psutil.disk_partitions()
        total = free = 0
        for p in partitions:
            if p.fstype != '':
                total = total + psutil.disk_usage(p.mountpoint).total
                free = free + psutil.disk_usage(p.mountpoint).free
        data["Total Disk Space"] = data["HD Size"] = str(math.floor(total / 2**30)) + " GB"
        data["Available Space"] = str(math.floor(free / 2**30)) + " GB"
        data["HD_Type"] = None

        try:
            data["Operating System"] = subprocess.check_output('systeminfo | findstr /B /C:"OS Name"',stderr=open(os.devnull, 'w'), shell=True).decode('utf-8').replace('  ','').partition('OS Name:')[2].strip(' \r\n')
        except Exception as error:
            data["Operating System"] = "{} {}".format(platform.system(), platform.release())
        try:
            data["Host Name"] = subprocess.check_output('ipconfig /all | findstr "Host Name"',stderr=open(os.devnull, 'w'), shell=True).decode('utf-8').partition(':')[2].strip(' ').strip('\r\n')
        except Exception as error:
            data["Host Name"] = None
        try:
            data["CPU_Core"] = str(subprocess.check_output('WMIC CPU Get NumberOfCores', stderr=open(os.devnull, 'w'), shell=True)).split()[1].strip('\\r\\n')
        except Exception as error:
            data["CPU_Core"] = None
        try:
            data["Manufacturer"] = str(subprocess.check_output('wmic computersystem get manufacturer', stderr=open(os.devnull, 'w'), shell=True)).split()[1].strip('\\r\\n')
        except Exception as error:
            data["Manufacturer"] = None
        try:
            data["Model"] = subprocess.check_output('wmic computersystem get model', stderr=open(os.devnull, 'w'), shell=True).decode('utf-8').partition('Model')[2].strip(' \r\n')
        except Exception as error:
            data["Model"] = None
        try:
            RAM = int(str(subprocess.check_output('wmic MemoryChip get MemoryType', stderr=open(os.devnull, 'w'), shell=True)).split()[1].strip('\\r\\n'))
            data["Ram_Type"] = RAM_Types[RAM]
        except Exception as error:
            data["Ram_Type"] = None
        try:
            ramSize = round(int(subprocess.check_output('systeminfo | findstr /C:"Total Physical Memory"', stderr=open(os.devnull, 'w'), shell=True).decode('utf-8').partition('Total Physical Memory:     ')[2].strip('\r\n').partition(' MB')[0].replace(',',''))/1024)
            data["Ram_Size"] = str(ramSize) + " GB"
        except Exception as error:
            data["Ram_Size"] = None
        try:
            data["Serial_Number"] = str(subprocess.check_output('wmic bios get serialnumber', stderr=open(os.devnull, 'w'), shell=True)).split()[1].strip('\\r\\n')
        except Exception as error:
            data["Serial_Number"] = None

        return data

    def getMacSystemSpec(self, data):
        """ Collect hardware info for Linux """

        data["Operating System"] = subprocess.check_output("sw_vers -productName",stderr=open(os.devnull, 'w'), shell=True).decode('utf-8').strip('\n')
        data["OS Version"] = subprocess.check_output("sw_vers -productVersion",stderr=open(os.devnull, 'w'), shell=True).decode('utf-8').strip('\n')
        data["Manufacturer"] = "Apple"

        try:
            data["Available Space"] = subprocess.check_output('system_profiler SPStorageDataType | grep Available', stderr=open(os.devnull, 'w'), shell=True).decode('utf-8').strip(' \n').partition('Available: ')[2].partition('(')[0].strip(' ')
        except Exception as error:
            data["Available Space"] = None
        try:
            data["Host Name"] = subprocess.check_output("hostname", stderr=open(os.devnull, 'w'), shell=True).decode('utf-8').strip('\n')
        except Exception as error:
            data["Host Name"] = None
        try:
            data["Ip"] = subprocess.check_output('route -n get 1 | grep interface | cut -d ":" -f2 | xargs ipconfig getifaddr', stderr=open(os.devnull, 'w'), shell=True).decode('utf-8').strip('\n')
        except Exception as error:
            data["Ip"] = None
        try:
            data["CPU_Core"] = str(subprocess.check_output("system_profiler SPHardwareDataType | grep 'Total Number of Cores:'", stderr=open(os.devnull, 'w'), shell=True)).split("Cores:")[1][1:-3]
        except Exception as error:
            data["CPU_Core"] = None
        try:
            data["HD Size"] = data["Total Disk Space"] = str(subprocess.check_output('system_profiler SPStorageDataType | grep Capacity', stderr=open(os.devnull, 'w'), shell=True)).split('Capacity:')[1].strip(' ').strip('\\n').split('(')[0]
        except Exception as error:
            data["HD Size"] = data["Total Disk Space"] = None
        try:
            data["Model"] = str(subprocess.check_output("system_profiler SPHardwareDataType | grep 'Model Name'", stderr=open(os.devnull, 'w'), shell=True)).split(':')[1][1:-3]
        except Exception as error:
            data["Model"] = None
        try:
            data["Ram_Type"] = str(subprocess.check_output('system_profiler SPMemoryDataType | grep Type', stderr=open(os.devnull, 'w'), shell=True)).split('Type:')[1].strip(' ').strip('\\n')
        except Exception as error:
            data["Ram_Type"] = None
        try:
            data["Ram_Size"] = subprocess.check_output('system_profiler SPHardwareDataType | grep "  Memory:"', stderr=open(os.devnull, 'w'), shell=True).decode('utf-8').partition('Memory: ')[2].strip('\n')
        except Exception as error:
            data["Ram_Size"] = None
        try:
            data["HD_Type"] = str(subprocess.check_output('system_profiler SPStorageDataType | grep Protocol', stderr=open(os.devnull, 'w'), shell=True)).split('Protocol:')[1].strip(' ')[:-3]
        except Exception as error:
            data["HD_Type"] = None
        try:
            data["Serial_Number"] = str(subprocess.check_output('system_profiler SPHardwareDataType | grep Serial', stderr=open(os.devnull, 'w'), shell=True)).split(':')[1][1:-3]
        except Exception as error:
            data["Serial_Number"] = None

        return data

os_info = SystemInfo()
sysInfo = os_info.systemSpec()

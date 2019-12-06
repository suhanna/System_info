# pyinstaller -F --hiddenimport=wmi itam.py : Windows
from tabulate import tabulate
import platform as p
import cpuinfo, subprocess, shutil
import os, re
import socket as sk
import multiprocessing

# https://winaero.com/blog/how-to-see-ddr-memory-type-in-command-prompt-in-windows-10/
RAM_Types = {
	0 : "Unknown",
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
    ''' System Informations'''
    def __init__(self):
        self.title = "System Management"

    def platformName(self):
        return p.system()

    def systemSpec(self):
        cinfo = cpuinfo.get_cpu_info()
        data = {}
        headers = ["System Information", ""]

        data["Processor"] = cinfo['brand']
        data["Total Disk Space"] = str(shutil.disk_usage("/")[0] // (2**30))+"GB"
        data["Available Space"] = str(shutil.disk_usage("/")[2] // (2**30))+"GB"
        data["CPU"] = cinfo['count']
        if os_info.platformName() == 'Linux':

            try:
                output = subprocess.check_call('PATH=$PATH:/bin:/sbin:/usr/bin:/usr/sbin:/usr/local/bin '
        'sudo dmidecode', stdout=DEVNULL, shell=True)
            except Exception as e:
                if str(e).find("command not found") == -1:
                    try:
                        subprocess.check_call(['sudo', 'apt-get', 'install', 'dmidecode'], stdout=open(os.devnull,'w'))
                    except subprocess.CalledProcessError as e:
                        print("dmidecode Installation Failed.")

            data["Operating System"] = p.version().split()[0].split('-')[1]
            data["OS Version"] = p.version().split()[0].split('-')[0].split('~')[1]
            try:
                Ip = str(subprocess.check_output("ip route get 1 | awk '{print $NF;exit}'",stderr=open(os.devnull, 'w'), shell=True))[2:-3]
            except Exception as  error:
                Ip = None
            try:
                CPU_Core = str(subprocess.check_output('lscpu | grep socket:', stderr=open(os.devnull, 'w'), shell=True)).split(':')[1][:-3]
            except Exception as  error:
                CPU_Core = None
            try:
                HD_Size = str(subprocess.check_output('sudo lshw -class disk | grep size', stderr=open(os.devnull, 'w'), shell=True)).split('(',1)[1].split(')')[0]
            except Exception as  error:
                HD_Size = None
            try:
                Manufacturer = str(subprocess.check_output('sudo dmidecode -s system-manufacturer', stderr=open(os.devnull, 'w'), shell=True))[2:-3]
            except Exception as  error:
                Manufacturer = None
            try:
                Model = str(subprocess.check_output('sudo dmidecode -s system-product-name', stderr=open(os.devnull, 'w'), shell=True))[2:-3]
            except Exception as  error:
                Model = None
            try:   
                Ram_Type = str(subprocess.check_output('sudo dmidecode -t 17 | grep -i type:', stderr=open(os.devnull, 'w'), shell=True)).split('\\tType:')[1].strip('\\n')
            except Exception as  error:
                Ram_Type = None
            try:
                HD_Type = str(subprocess.check_output('sudo lshw -class disk -class storage | grep description', stderr=open(os.devnull, 'w'),shell=True)).split('\\n')[0].split(':')[1]
            except Exception as  error:
                HD_Type = None
            try:
                Serial_Number = str(subprocess.check_output('sudo dmidecode -s system-serial-number', stderr=open(os.devnull, 'w'), shell=True))[2:-3]
            except Exception as  error:
                Serial_Number = None
        elif os_info.platformName() == 'Windows':
            Ip = sk.gethostbyname(sk.gethostname())
            data["Operating System"] = p.system()
            data["OS Version"] = p.version()
            try:
            	CPU_Core = str(subprocess.check_output('WMIC CPU Get NumberOfCores', stderr=open(os.devnull, 'w'), shell=True)).split()[1].strip('\\r\\n')
            except Exception as  error:
                CPU_Core = None

            HD_Size = str(shutil.disk_usage("/")[0] // (2**30))+"GB"
            HD_Type = None

            try:
                Manufacturer = str(subprocess.check_output('wmic computersystem get manufacturer', stderr=open(os.devnull, 'w'), shell=True)).split()[1].strip('\\r\\n')
            except Exception as  error:
                Manufacturer = None
            try:
                Model = str(subprocess.check_output('wmic computersystem get model', stderr=open(os.devnull, 'w'), shell=True)).split()[1].strip('\\r\\n')
            except Exception as  error:
                Model = None
            try:   
                RAM = int(str(subprocess.check_output('wmic MemoryChip get MemoryType', stderr=open(os.devnull, 'w'), shell=True)).split()[1].strip('\\r\\n'))
                Ram_Type  = RAM_Types[RAM]
            except Exception as  error:
                Ram_Type = None
            try:
                Serial_Number = str(subprocess.check_output('wmic bios get serialnumber', stderr=open(os.devnull, 'w'), shell=True)).split()[1].strip('\\r\\n')
            except Exception as  error:
                Serial_Number = None

        data["Ip"] = Ip
        data["CPU_Core"] = CPU_Core
        data["HD Size"] = HD_Size
        data["Manufacturer"] = Manufacturer
        data["Model"] = Model
        data["RAM"] = Ram_Type
        data["HD_Type"] = HD_Type
        data["Serial_Number"] = Serial_Number
        return data

os_info = SystemInfo()
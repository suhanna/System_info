# System_info

This is a module which can provide following system informations.  
1. Processor
2. Total Disk Space
3. Available Space
4. CPU
5. Operating System
6. OS Version
7. Ip
8. CPU_Core
9. HD Size
10. Manufacturer
11. Model
12. RAM
13. HD Type
14. Serial_Number

It can be used as

    from system_info import os_info
    os_info.systemSpec()
>{'Processor': 'Intel(R) Core(TM) i3-5005U CPU @ 2.00GHz', 'Total Disk Space': '454GB', 'Available Space': '305GB', 'CPU': 4, 'Operating System': 'Ubuntu', 'OS Version': '14.04.1', 'Ip': '192.168.10.116', 'CPU_Core': '    2', 'HD Size': '500GB', 'Manufacturer': 'Dell Inc.', 'Model': 'Latitude 3560', 'RAM': ' DDR3', 'HD_Type': ' SATA controller', 'Serial_Number': '9PCHZB2'}

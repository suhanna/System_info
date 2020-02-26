system_info
===========

- system_info is a package for finding system hardware specifications.
- It is cross-platform package, which you can run on Linux, Windows and macOS.

**Note:** For Linux system it requires sudo user password and dmidecode should be installed.

###### system_info provides following information ######

* Processor
* CPU (Total CPU count)
* Total Disk Space
* Available Space
* Host Name
* Ip
* Operating System
* OS Version
* CPU_Core
* HD Size
* Manufacturer
* Model
* Ram_Type
* Ram_Type
* HD Type
* Serial_Number

It can be used as
```python
from system_info import sysinfo
system_hardware_details = sysinfo.sysInfo
```
Sample result for Linux :
>{'Processor': 'Intel(R) Core(TM) i3-5005U CPU @ 2.00GHz', 'CPU': 4, 'Total Disk Space': '454GB', 'Available Space': '231GB', 'Host Name': 'XXXXX', 'Ip': 'xxx.xxx.xx.xxx', 'Operating System': 'Ubuntu', 'OS Version': '14.04', 'CPU_Core': '2', 'HD Size': '500GB', 'Manufacturer': 'Dell Inc.', 'Model': 'Latitude 3560', 'Ram_Type': 'DDR3', 'Ram_Size': '8 GB', 'HD_Type': 'SATA controller', 'Serial_Number': 'XXXXXXX'}

Sample result for Windows :
>{'Processor': 'Intel(R) Core(TM) i3-5005U CPU @ 2.00GHz', 'CPU': 1, 'Ip': 'xxx.xxx.xx.xxx', 'OS Version': '10.0.10240', 'Total Disk Space': '49 GB', 'HD Size': '49 GB', 'Available Space': '36 GB', 'HD_Type': None, 'Operating System': 'Microsoft Windows 10 Pro', 'Host Name': 'XXXXX', 'CPU_Core': '1', 'Manufacturer': 'Dell Inc.', 'Model': 'Latitude 3560', 'Ram_Type': DDR3, 'Ram_Size': '8 GB', 'Serial_Number': 'XXXXXXX'}

Sample result for MacOS :
>{'Processor': 'Intel(R) Core(TM) i5-4278U CPU @ 2.60GHz', 'CPU': 4, 'Operating System': 'Mac OS X', 'OS Version': '10.14.6', 'Manufacturer': 'Apple', 'Available Space': '891.64 GB', 'Host Name': 'XXXXX', 'Ip': 'xxx.xxx.xx.xxx', 'CPU_Core': '2', 'HD Size': '1 TB ', 'Total Disk Space': '1 TB ', 'Model': 'Mac mini', 'Ram_Type': 'DDR3', 'Ram_Size': '8 GB', 'HD_Type': 'SATA', 'Serial_Number': 'XXXXXXX'}
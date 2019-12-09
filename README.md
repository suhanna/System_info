system_info
===========

- This is a module which can provide following system informations.
- For Linux system it requires sudo user password.
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
```python
from system_info import sysinfo
system_details = sysinfo.os_info.systemSpec()
```
Sample output will look like below,
>> {'Processor': 'Intel(R) Core(TM) i3-5005U CPU @ 2.00GHz', 'Total Disk Space': '454GB', 'Available Space': '304GB', 'CPU': 4, 'Operating System': 'Ubuntu', 'OS Version': '14.04.1', 'Ip': '192.168.10.116', 'CPU_Core': '    2', 'HD Size': '500GB', 'Manufacturer': 'Dell Inc.', 'Model': 'Latitude 3560', 'RAM': ' DDR3', 'HD_Type': ' SATA controller', 'Serial_Number': '9PCHZB2'}

## Monitoring of system params from the terminal.

### Description
A script for displaying system indicators in tabular form.
It is an add-on to the psutils library.

**Attention:** Python 3.6+ version required

#### Metrics
- General information (hostname, uptime, la)
- System information:
  - CPU
  - RAM
  - Swap
  - Interfaces
  - Disk usage
- Active user connections
- OPTIONAL: Information about the state of the application under protein-daemon
  - General information (pid, name, status, )
  - XMS, XMX (JVM opts)


### Features
- Tabular representation
- Color indication of tresholds

### Usage
#### Installation:
It is recommended to use a virtual environment:
```shell
pip install -r requirements.txt
```

#### Usage:
```shell
python3 ./run.py
```

#### Customization:
It is possible to change the color values for the supported thresholds according to the implemented metrics.
(Unfortunately, it will not be possible to add your own thresholds without changing the code)
More info in lib/enums.p

### Output example
```bash
+Common metrics-------+------------+--------------+
| Hostname            | Uptime     | Load Average |
+---------------------+------------+--------------+
| great_hostname      | up 66 days | 1m: 0.22     |
|                     |            | 5m: 0.2      |
|                     |            | 15m: 0.22    |
+---------------------+------------+--------------+
+Virtual Memory-----+---------+------+--------+--------+----------+---------+--------+--------+--------+
| total | available | percent | used | free   | active | inactive | buffers | cached | shared | slab   |
+-------+-----------+---------+------+--------+--------+----------+---------+--------+--------+--------+
| 7.6G  | 2.2G      | 71.1B   | 5.1G | 767.3M | 4.5G   | 1.8G     | 0.0B    | 1.7G   | 124.0K | 256.0M |
+-------+-----------+---------+------+--------+--------+----------+---------+--------+--------+--------+
+Swap Memory-----+------+---------+--------+--------+
| total | used   | free | percent | sin    | sout   |
+-------+--------+------+---------+--------+--------+
| 1.6G  | 363.2M | 1.2G | 22.1B   | 188.4M | 509.7M |
+-------+--------+------+---------+--------+--------+
+CPU ------+------+----------+------------+---------+-----+---------+--------+-------+------------+
| user     | nice | system   | idle       | iowait  | irq | softirq | steal  | guest | guest_nice |
+----------+------+----------+------------+---------+-----+---------+--------+-------+------------+
| 26867.13 | 0.09 | 17431.19 | 1409342.29 | 3168.3  | 0.0 | 2482.35 | 540.3  | 0.0   | 0.0        |
| 24859.36 | 0.25 | 30694.62 | 1411761.11 | 2849.58 | 0.0 | 493.06  | 250.5  | 0.0   | 0.0        |
| 24227.73 | 0.53 | 14402.52 | 1421786.88 | 3918.62 | 0.0 | 783.23  | 344.02 | 0.0   | 0.0        |
| 21571.48 | 0.4  | 28899.27 | 1418070.37 | 2981.32 | 0.0 | 60.75   | 200.65 | 0.0   | 0.0        |
| 23291.54 | 0.2  | 14017.89 | 1424065.04 | 3324.8  | 0.0 | 795.85  | 321.41 | 0.0   | 0.0        |
| 22826.01 | 0.41 | 29833.71 | 1414892.54 | 3223.38 | 0.0 | 264.35  | 220.59 | 0.0   | 0.0        |
| 25200.17 | 0.32 | 15301.99 | 1418741.13 | 3209.81 | 0.0 | 1372.88 | 397.52 | 0.0   | 0.0        |
| 21845.81 | 0.03 | 29852.56 | 1416501.66 | 3203.67 | 0.0 | 59.85   | 206.79 | 0.0   | 0.0        |
+----------+------+----------+------------+---------+-----+---------+--------+-------+------------+
+Disk--------------+---------+--------+--------+---------+
| path             | total   | used   | free   | percent |
+------------------+---------+--------+--------+---------+
| /                | 13.4G   | 5.1G   | 8.3G   | 38.2    |
| /boot            | 1014.0M | 182.6M | 831.4M | 18.0    |
| /usr/test/cdr    | 40.0G   | 4.0G   | 36.0G  | 10.0    |
| /usr/test/logs   | 40.0G   | 4.1G   | 35.9G  | 10.2    |
+------------------+---------+--------+--------+---------+
+Interfaces-----------+---------------+--------+
| name | address      | netmask       | family |
+------+--------------+---------------+--------+
| lo   | 127.0.0.1    | 255.0.0.0     | ipv4   |
| eth0 | 192.168.73.2 | 255.255.128.0 | ipv4   |
+------+--------------+---------------+--------+
+Connected Users--+----------------+--------------+--------+
| name | terminal | host           | started      | pid    |
+------+----------+----------------+--------------+--------+
| root | tty1     |                | 1619470720.0 | 1308   |
| root | pts/3    | 192.168.100.10 | 1620924160.0 | 106264 |
+------+----------+----------------+--------------+--------+
```

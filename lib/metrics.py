"""Contains methods for statistic collection. Add-on to the psutils module."""

import datetime
import json
import os
from collections import namedtuple as cnt
from socket import AF_INET
from typing import List, TypeVar, NamedTuple, Tuple

import psutil
from psutil._common import suser as SUSER

from config import DAEMON_SERVICE_LIST
from lib.utils import run_command, namedtuple_bytes_to_human

DAEMON_SERVICE_TYPE = cnt('service', ['name', 'process', 'process_stat'])
NIC_TYPE = cnt('ipaddr', ['name', 'address', 'netmask', 'family'])
DISK_TYPE = cnt('disk', ['path', 'sdiskpart', 'sdiskusage'])

T = TypeVar("T")

__all__ = ['get_uptime',
           'get_hostname',
           'get_load_avg',
           'get_cpu_count',
           'get_cpu_stat',
           'get_connected_users',
           'get_disk_stat',
           'get_swap_memory_stat',
           'get_ip_address',
           'get_daemon_apps_stat',
           'get_virtual_memory_stat',
           ]


def get_uptime() -> str:
    return " ".join([x.replace(',', '') for x in run_command('uptime').split()[1:4]])


def get_hostname() -> str:
    return run_command(cmd='hostname')


def get_cpu_count(*, logical: bool = False) -> int:
    return int(psutil.cpu_count(logical=logical))


def get_cpu_stat(*, percpu=False) -> List[NamedTuple]:
    cpus_stat = psutil.cpu_times(percpu=percpu)
    if not isinstance(cpus_stat, list):
        return [cpus_stat]
    return cpus_stat


def get_load_avg(*, percentage: bool = False) -> List[float]:
    load_avg = psutil.getloadavg()
    if percentage:
        load_avg = [_value / get_cpu_count(logical=True) * 100 for _value in load_avg]

    return list(load_avg)


def get_connected_users(*, epoch2date: bool = False) -> List[SUSER]:
    users = psutil.users()
    if epoch2date:
        for i, user in enumerate(users):
            users[i] = user._replace(
                started=datetime.datetime.fromtimestamp(user.started).strftime("%Y-%m-%d %H:%M:%S"))
    return users


def get_virtual_memory_stat(*, bytes2human: bool = False, exclude: Tuple = ()) -> NamedTuple:
    virtual_mem = psutil.virtual_memory()

    if bytes2human:
        virtual_mem = namedtuple_bytes_to_human(virtual_mem, exclude)

    return virtual_mem


def get_swap_memory_stat(*, bytes2human: bool = False, exclude: Tuple = ()) -> NamedTuple:
    swap_mem = psutil.swap_memory()

    if bytes2human:
        swap_mem = namedtuple_bytes_to_human(swap_mem, exclude)

    return swap_mem


def get_disk_stat(*, bytes2human: bool = False) -> List[DISK_TYPE]:
    ret_list = []
    for partition in psutil.disk_partitions():
        disk_usage = psutil.disk_usage(partition.mountpoint)

        if bytes2human:
            disk_usage = namedtuple_bytes_to_human(disk_usage, exclude=('percent',))

        ret_list.append(DISK_TYPE(path=partition.mountpoint, sdiskpart=partition, sdiskusage=disk_usage))
    return ret_list


def get_ip_address(interface: str = '') -> List[NIC_TYPE]:
    net_addresses = psutil.net_if_addrs()
    ret_list = []

    if interface:
        try:
            net_interface = {interface: net_addresses[interface]}
        except KeyError:
            net_interface = net_addresses
    else:
        net_interface = net_addresses

    for name, interf in net_interface.items():
        for addr in interf:
            if addr.family is AF_INET:
                ret_list.append(NIC_TYPE(name=name, address=addr.address, netmask=addr.netmask, family='ipv4'))

    return ret_list


def get_daemon_apps_stat() -> List[DAEMON_SERVICE_TYPE]:
    """
    Get application statistics run by protei-daemon app if config.DAEMON_ENABLED is True

    Returns: List of services
    """
    return __match_processes_with_service_names(__get_daemon_service_names(exclude_defaults=True))


def __get_daemon_service_names(*, exclude_defaults: bool = True) -> List[DAEMON_SERVICE_TYPE]:
    services = run_command("protei-daemon list --filter all")
    ret_list = []
    for service in services.split('\n'):
        name = service.strip()

        if not name:
            continue

        if exclude_defaults:
            if name not in DAEMON_SERVICE_LIST:
                ret_list.append(DAEMON_SERVICE_TYPE(name=name, process=None, process_stat=None))
        else:
            ret_list.append(DAEMON_SERVICE_TYPE(name=name, process=None, process_stat=None))

    return ret_list


def __match_processes_with_service_names(services: List[DAEMON_SERVICE_TYPE]) -> List[DAEMON_SERVICE_TYPE]:
    for _i, _service in enumerate(services):
        _service_pid = None
        _process = None
        try:
            _service_config = json.loads(run_command(f"protei-daemon get_service_config {_service.name}"))
            _service_pid_path = os.path.join(_service_config['env']['SERVICE_TMP_DIR'], "application.pid")
            with open(_service_pid_path, 'r') as f:
                _service_pid = int(f.read().strip().replace('\n', ''))

            if psutil.pid_exists(_service_pid):
                _process = psutil.Process(pid=_service_pid)
                services[_i] = services[_i]._replace(process=_process)
                services[_i] = services[_i]._replace(process_stat=__get_process_stat(_process))
        except Exception:
            continue
    return services


def __get_jvm_opts(p: psutil.Process):
    _p_stat = {}
    _cmdline = p.cmdline()
    _opts = ' '.join(_cmdline)
    _xms_shift = _opts.find('Xms')
    _xmx_shift = _opts.find('Xmx')
    try:
        _p_stat.update({"xms": _opts[_xms_shift + 3:_xms_shift + 10].split(' ')[0]})
    except Exception:
        pass
    try:
        _p_stat.update({"xmx": _opts[_xmx_shift + 3:_xmx_shift + 10].split(' ')[0]})
    except Exception:
        pass
    return _p_stat


def __get_process_stat(p: psutil.Process):
    _p_stats = {}
    _p_stats.update(__get_jvm_opts(p))
    return _p_stats

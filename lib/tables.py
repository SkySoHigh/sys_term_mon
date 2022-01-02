"""Contains methods for converting the collected statistics to a tabular form."""

import json
from typing import NamedTuple, NoReturn, List

from terminaltables import AsciiTable

from config import DAEMON_ENABLED
from lib.colors import Colorize
from lib.enums import Thresholds
from lib.metrics import get_hostname, get_uptime, get_load_avg, get_ip_address, get_connected_users, get_cpu_stat, \
    get_virtual_memory_stat, get_cpu_count, get_swap_memory_stat, get_disk_stat, get_daemon_apps_stat
from lib.utils import pprint_secs


def namedtuple_list_to_table(nt: List[NamedTuple], table_title: str = "") -> AsciiTable:
    if not table_title:
        table_title = None
    return AsciiTable(title=table_title, table_data=[nt[0]._fields, *nt])


def common_metrics_to_table() -> AsciiTable:
    _table = AsciiTable(title="Common metrics", table_data=[])
    try:
        _hostname = get_hostname()
        _uptime = get_uptime()
        _la_str_repr = "\n".join(
            list(map(lambda _value, _key: str(_value) + ": " + Colorize.by_thresholds(_key, Thresholds.load_average),
                     ["1m", "5m", "15m"], get_load_avg())))
    except Exception:
        _table.table_data = [["Unable to collect common metrics"]]
        return _table

    _table.table_data = [
        ["Hostname", "Uptime", "Load Average"],
        [_hostname, _uptime, _la_str_repr]
    ]
    return _table


def disk_metrics_to_table(*, bytes2human: bool = False) -> AsciiTable:
    _table = AsciiTable(title="Disk", table_data=[])
    _table.inner_row_border = True

    try:
        _d_stats = get_disk_stat(bytes2human=bytes2human)
    except Exception:
        _table.table_data = [["Unable to collect disk metrics"]]
        return _table

    _data = []

    for _disk in _d_stats:
        _data.append([_disk.path, _disk.sdiskusage[0], _disk.sdiskusage[1], _disk.sdiskusage[2],
                      Colorize.by_thresholds(_disk.sdiskusage[3], Thresholds.disk)])

    _headers = ["path"]
    _headers.extend(_d_stats[0].sdiskusage._fields)

    _table.table_data = [
        _headers,
        *_data
    ]

    return _table


def app_metric_to_table() -> AsciiTable:
    _table = AsciiTable(title="Application Statistic", table_data=[])
    _table.inner_row_border = True

    try:
        _app_stats = get_daemon_apps_stat()
    except Exception:
        _table.table_data = [["Unable to collect protei-daemon applications metrics"]]
        return _table

    _headers = ["Pid", "Name", "Status", "Started"]
    _stat_headers = []
    _data = []
    for _app in _app_stats:
        if _app.process is not None:

            if not _stat_headers:
                if _app.process_stat:
                    _stat_headers = _app.process_stat.keys()
                    _headers.extend(_stat_headers)

            _data.append(
                [_app.process.pid, _app.name, _app.process.status(), pprint_secs(int(_app.process._create_time)),
                 *_app.process_stat.values()])
        else:
            _data.append([None, _app.name, "not running", None])

    for i, v in enumerate(_data):
        for si, sv in enumerate(v):
            if isinstance(sv, dict):
                _data[i][si] = json.dumps(sv, indent=1)
    _table.table_data = [
        _headers,
        *_data
    ]

    return _table


def show_stat_tables() -> NoReturn:
    print(common_metrics_to_table().table)

    print(namedtuple_list_to_table([get_virtual_memory_stat(bytes2human=True)], table_title="Virtual Memory").table)

    swap_mem = get_swap_memory_stat(bytes2human=True)
    swap_mem = swap_mem._replace(
        **{swap_mem._fields[3]: Colorize.by_thresholds(metric=swap_mem[3], threshold=Thresholds.swap_memory)})
    print(namedtuple_list_to_table([swap_mem], table_title="Swap Memory").table)

    print(namedtuple_list_to_table(get_cpu_stat(percpu=True), table_title=f"CPU's {get_cpu_count(logical=True)}").table)
    print(disk_metrics_to_table(bytes2human=True).table)
    print(namedtuple_list_to_table(get_ip_address(), table_title="Interfaces").table)
    print(namedtuple_list_to_table(get_connected_users(epoch2date=True), table_title="Connected Users").table)

    if DAEMON_ENABLED:
        print(app_metric_to_table().table)

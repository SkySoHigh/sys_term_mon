"""Various helpful methods."""

import datetime
import subprocess
import time
from typing import TypeVar, NamedTuple, Tuple

T = TypeVar("T")


def bytes_to_human(n: T, *, format="%(value).1f%(symbol)s") -> str:
    _symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    _prefix = {}
    for _i, _symbol in enumerate(_symbols):
        _prefix[_symbol] = 1 << (_i + 1) * 10
    for _symbol in reversed(_symbols):
        if n >= _prefix[_symbol]:
            _value = float(n) / _prefix[_symbol]
            return '%.1f%sB' % (_value, _symbol)
    return "%s" % n


def run_command(cmd: str) -> str:
    try:
        _run = subprocess.Popen(cmd.split(" "), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        _stdout, _ = _run.communicate()
        return _stdout.decode('utf8')
    except Exception as e:
        print(f"Command can not be executed: {cmd}")
        print(f"Error occurred: {e.args}")
        raise e


def namedtuple_bytes_to_human(nt: NamedTuple, exclude: Tuple = ()) -> NamedTuple:
    _tuple_fields = [_field for _field in nt._fields if _field not in exclude]
    for _field in _tuple_fields:
        _value = getattr(nt, _field)
        nt = nt._replace(**{_field: bytes_to_human(_value)})
    return nt


def pprint_secs(secs: int) -> str:
    _now = time.time()
    _secs_ago = int(_now - secs)
    if _secs_ago < 60 * 60 * 24:
        _fmt = "%H:%M:%S"
    else:
        _fmt = "%Y-%m-%d %H:%M:%S"
    return datetime.datetime.fromtimestamp(secs).strftime(_fmt)

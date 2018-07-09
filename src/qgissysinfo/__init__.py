import os

import qgissysinfo.systeminfo
import qgissysinfo.qgisinfo


def info():
    _info = systeminfo.allSystemInfo()
    _info.update(qgisinfo.allQgisInfo())
    return _info


def _as_text(o, level = 0):
    if isinstance(o, dict):
        s = ""
        for key,value in o.items():
            s += ("\t" * level)
            s += "-" + key + os.linesep
            s += _as_text(value, level + 1)
        return s
    elif isinstance(o, list):
        s = ""
        for item in o:
            s += _as_text(item, level)
        return s
    else:
        return ("\t" * level) + "-" + str(o) + os.linesep


def info_as_text():
    return _as_text(info())

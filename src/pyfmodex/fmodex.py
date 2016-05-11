from ctypes import *
import os
import platform
from . import globalvars
from .utils import ckresult
from .structobject import Structobject as so


arch = platform.architecture()[0]

if os.name == 'nt':
    if arch == '32bit':
        # print("[FMODEX] Loading : %s" % "default")
        # _dll = windll.fmodex
        print("[FMODEX] Loading : %s" % "../assets/lib/fmodex.dll")
        print("[FMODEX] Exists  : %s" % os.path.exists("../assets/lib/fmodex.dll"))
        _dll = CDLL("../assets/lib/fmodex.dll")
    else:
        # print("[FMODEX] Loading : %s" % "default x64")
        # _dll = windll.fmodex64
        print("[FMODEX] Loading : %s" % "../assets/lib/fmodex64.dll")
        print("[FMODEX] Exists  : %s" % os.path.exists("../assets/lib/fmodex64.dll"))
        _dll = CDLL("../assets/lib/fmodex64.dll")
elif os.name == 'posix':
    if arch == '32bit':
        print("[FMODEX] Loading : %s" % "../assets/lib/libfmodex.so")
        print("[FMODEX] Exists  : %s" % os.path.exists("../assets/lib/libfmodex.so"))
        _dll = CDLL('../assets/lib/libfmodex.so')
    else:
        print("[FMODEX] Loading : %s" % "../assets/lib/libfmodex64.so")
        print("[FMODEX] Exists  : %s" % os.path.exists("../assets/lib/libfmodex64.so"))
        _dll = CDLL('../assets/lib/libfmodex64.so')
else:
    raise RuntimeError("Can not load FMODEX on this Operating system")

globalvars.dll = _dll


def get_debug_level():
    """Returns the current debug level.
    :rtype: integer
    """
    level = c_int()
    ckresult(_dll.FMOD_Debug_GetLevel(byref(level)))
    return level.value


def set_debug_level(level):
    """Sets the current debug level.
    :param level: The level to set.
    """
    ckresult(_dll.FMOD_Debug_SetLevel(level))


def get_disk_busy():
    """Gets the busy status of the disk.
    :returns: Whether the disk is busy.
    :rtype: boolean
    """
    busy = c_int()
    ckresult(_dll.FMOD_File_GetDiskBusy(byref(busy)))
    return busy.value


def set_disk_busy(busy):
    """Sets the busy status.
    :param busy: The busy status.
    :type busy: boolean
"""
    ckresult(_dll.FMOD_File_SetDiskBusy(busy))


def get_memory_stats(blocking):
    """Returns the current memory stats.
    :param blocking: Gather more accurate stats, but perhaps don't return inmediately.
    :type blocking: boolean
    :returns: A StructObject with the values current and maximum.
    """
    current = c_int()
    max = c_int()
    ckresult(_dll.FMOD_Memory_GetStats(byref(current), byref(max), blocking))
    return so(current=current.value, maximum=max.value)


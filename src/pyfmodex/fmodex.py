from ctypes import *
import os
import platform
from . import globalvars
from .utils import ckresult
from .structobject import Structobject as so


arch = platform.architecture()[0]

if os.name == 'nt':
    if arch == "32bit":
        _dll = CDLL('../assets/lib/fmod.dll')
    else:
        _dll = CDLL('../assets/lib/fmod64.dll')
elif os.name == "posix":
    if arch == "32bit":
        _dll = CDLL('../assets/lib/libfmodex.so')
    else:
        _dll = CDLL('../assets/lib/libfmodex64.so')

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


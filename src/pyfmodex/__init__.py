"""Fmod ex python bindings."""
from .fmodex import get_debug_level, set_debug_level, get_disk_busy, set_disk_busy, get_memory_stats
from . import globalvars
# Avoid recursive import hell
from . import dsp, dsp_connection, geometry, channel, channel_group, reverb, sound, sound_group, system

__version__ = "0.3.3"

c = {
    "DSP": dsp.DSP,
    "DSP_Connection": dsp_connection.DSPConnection,
    "Geometry": geometry.Geometry,
    "Channel": channel.Channel,
    "ChannelGroup": channel_group.ChannelGroup,
    "Reverb": reverb.Reverb,
    "Sound": sound.Sound,
    "SoundGroup": sound_group.SoundGroup,
    "System": system.System
}
globalvars.class_list = c
from . import constants, utils

System = c["System"]
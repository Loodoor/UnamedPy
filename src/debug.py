__author__ = 'Folaefolc'
"""
Code par Folaefolc
Licence MIT
"""

from constantes import DEBUG_LEVEL, ree, POL_ANTIALISING


def println(*args, sep=" ", end="\r\n"):
    if DEBUG_LEVEL >= 1:
        print(*args, sep=sep, end=end)


def onscreen_debug(ecran, font, *debug_infos, **kwargs):
    if DEBUG_LEVEL >= 2:
        start_y = kwargs.get("y", 0)
        start_x = kwargs.get("x", 0)
        size_y = kwargs.get("sy", -1)
        line_height = kwargs.get("line_height", 18)
        line_width = kwargs.get("line_width", 150)
        if size_y == -1:
            ree.draw_rect(ecran, (start_x, start_y, line_width, len(debug_infos) * line_height), (128, 128, 128))
        else:
            ree.draw_rect(ecran, (start_x, start_y, line_width, size_y), (128, 128, 128))
        for count, info in enumerate(debug_infos):
            ecran.blit(font.render(str(info), POL_ANTIALISING, (10, 10, 10)), (start_x, start_y + count * line_height))
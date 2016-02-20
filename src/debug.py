__author__ = 'Folaefolc'
"""
Code par Folaefolc
Licence MIT
"""

from constantes import DEBUG_LEVEL


def println(*args, sep=" ", end="\r\n"):
    if DEBUG_LEVEL == 1:
        print(*args, sep=sep, end=end)
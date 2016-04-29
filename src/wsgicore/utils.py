__author__ = 'Folaefolc'
"""
Code par Folaefolc
Licence MIT
"""

from contextlib import contextmanager, redirect_stdout
from wsgiref.simple_server import make_server
import webbrowser
from io import StringIO

from .constants import *


def normalize(content):
    if isinstance(content, str):
        return normalize(content.split('\n'))
    return [str(line).encode(UTF8_ENCODAGE) for line in content]


@contextmanager
def tag(name: str, stream: StringIO, **style):
    with redirect_stdout(stream):
        if style:
            print("<%s %s>" % (name, ' '.join("%s='%s'" % (k, v) for k, v in style.items())), end='')
        else:
            print("<%s>" % name)
        yield
        print("</%s>" % name, end='')


def create_server(addr: str="localhost", port: int=5500, rooter: object=None):
    if rooter:
        print("Starting on {}:{}".format(addr, port))
        serv_http = make_server(addr, port, rooter)
        webbrowser.open("http://{}:{}".format(addr, port))
        return serv_http
    raise ValueError("Le rooter doit être défini !")


def not_found(env, resp):
    resp(page_not_found, HTML_PAGE)
    s = StringIO()
    with tag("html", s):
        with tag("body", s):
            with tag("center", s):
                with tag("h1", s, style="background-color: red;"):
                    print("Erreur 404")
                print("La page n'a pas pu être trouvée ...")
    return normalize(s.getvalue())


def create_router(**routes):
    def rooter(env, resp):
        pages = routes
        for addr, view in pages.items():
            if env['PATH_INFO'] == addr:
                return view(env, resp)

        return not_found(env, resp)
    return rooter
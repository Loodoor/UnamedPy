__author__ = 'Folaefolc'
"""
Code par Folaefolc
Licence MIT
"""

from wsgicore.utils import *


def create_header(stream: StringIO, titre: str):
    with tag("head", stream):
        with tag("title", stream):
            print("Unamed - {}".format(titre))
        print("<meta charset='utf-8'/>")


def index(env, resp):
    resp(ok, HTML_PAGE)
    s = StringIO()
    with tag("html", s):
        create_header(s, "Serveur")
        with tag("body", s):
            with tag("p", s, style="background-color: red;", width="50%", center="center"):
                print("Ceci est l'index web du serveur d'Unamed")
            with tag("p", s):
                print("Pages disponnibles :")
                with tag("ul", s):
                    pages = ['/', '/info', '/doc']
                    for page in pages:
                        print("<li><a href='%s'>%s</a></li>" % (page, page))

    return normalize(s.getvalue())


def info(env, resp):
    resp(ok, HTML_PAGE)
    s = StringIO()
    with tag("html", s):
        create_header(s, "Serveur")
        with tag("body", s):
            with tag("p", s):
                print("Aucune information disponnible pour le moment")
    return normalize(s.getvalue())


def doc(env, resp):
    resp(ok, HTML_PAGE)
    s = StringIO()
    with tag("html", s):
        create_header(s, "Documentation")
        with tag("body", s):
            with tag("p", s, style="border: dashed;"):
                print("Pas encore de documentatio pour le moment")
    return normalize(s.getvalue())


pages_dict = {
    '/': index,
    '/info': info,
    '/doc': doc
}
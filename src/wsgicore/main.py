__author__ = 'Folaefolc'
"""
Code par Folaefolc
Licence MIT
"""

import time

from .utils import *
from . import forms

# CODE DE TEST UNIQUEMENT


def create_header(stream: StringIO):
    with tag("head", stream):
        with tag("title", stream):
            print("Un zoli site fait main !")


def index(env, resp):
    resp(ok, HTML_PAGE)
    s = StringIO()
    with tag("html", s):
        create_header(s)
        with tag("body", s):
            with tag("p", s, style="background-color: red;", width="50%", center="center"):
                print("Hello world !", end="<br />")
                print("Il est {} !".format(time.strftime("%H:%M:%S")), end="<br />")
                with tag("i", s):
                    print("Je suis un beau texte en italic !", end="<br />")
                    print("Moi aussi !", end="<br />")
                with tag("b", s):
                    print("Sauf que moi j'ai le swag et que je suis en gras héhé ^^", end="<br />")
            with tag("div", s, style="background-color: blue;"):
                print("Petit Menu !", end="<br />")
                print("Pages disponnibles :", end="<br />")
                with tag("ul", s):
                    elems = [
                        "index",
                        "pseudo",
                        "info"
                    ]
                    for elem in elems:
                        print("<li>%s</li>" % elem)
    return normalize(s.getvalue())


def pseudo(env, resp):
    resp(ok, HTML_PAGE)
    return forms.test_form(env, resp, ('127.0.0.1', 5500))


def info(env, resp):
    resp(ok, HTML_PAGE)
    s = StringIO()
    with tag("html", s):
        create_header(s)
        with tag("body", s):
            with tag("p", s, style="border: dashed;"):
                print("Bonjour ! Ce site a été entièrement créé grâce à une lib fait main !", end="<br />")
                print("Si toi aussi tu veux essayer cette lib, c'est par ici : ", end='')
                with tag("a", s, href="https://github.com/Loodoor/wsgi_test"):
                    print("clic moi !", end='<br />')
                print("Tout le code de ce site se trouve dans le fichier main.py du package core :)")
    return normalize(s.getvalue())


def rooter(env, resp):
    pages = {
        '/': index,
        '/pseudo': pseudo,
        '/info': info
    }

    for addr, view in pages.items():
        if env['PATH_INFO'] == addr:
            return view(env, resp)

    return not_found(env, resp)
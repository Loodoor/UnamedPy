__author__ = 'Folaefolc'
"""
Code par Folaefolc
Licence MIT
"""

import cgi
import html

from .utils import *


def form_builder(label, text_field_name, redirect_to, env):
    formulaire = cgi.FieldStorage(fp=env['wsgi.input'], environ=env)
    s = StringIO()

    if text_field_name in formulaire:
        with tag("", s):
            print(html.escape(formulaire.getvalue(text_field_name, "")))
        return normalize(s.getvalue())
    else:
        with tag("form", s, method="get", action="/{redirect}".format(redirect=redirect_to)):
            with tag("label", s):
                print(label)
            print("<input name='{field_name}' />".format(field_name=text_field_name))
        return normalize(s.getvalue())


def test_form(env, resp, addr):
    return form_builder("Un pseudo", "pseudo", ':'.join(str(i) for i in addr) + "/pseudo", env)
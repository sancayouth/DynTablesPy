# -*- coding: utf-8 -*-
import urllib

def formToDict(form):
    fdict = {}
    for l in urllib.unquote(form).split('&'):
        val = l.split('=')
        if val[1] != '':
            fdict[val[0]] = val[1]
    return fdict

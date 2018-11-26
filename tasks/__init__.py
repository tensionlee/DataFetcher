from WindPy import w
if not w.isconnected():
    w.start()


__all__ = ["uqerClient", 'DataAPI']

import uqer
from uqer import DataAPI
uqerClient = uqer.Client(token='89cb8ba68374b2ad3f02be301b7bdd10a5e333f6a9b15ec5c622578a5832b54c')
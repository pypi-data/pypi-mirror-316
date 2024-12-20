from .cli.cli import init
import sys


try:
    get_ipython
except NameError:
    init()



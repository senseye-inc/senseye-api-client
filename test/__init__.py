from logging import getLogger, WARNING
from . utils.docker import clean_up
getLogger('matplotlib').setLevel(WARNING)

def setUp():
    clean_up()

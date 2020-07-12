from cc import import_file

_lib = import_file('_lib.py', __file__)

_lib._computer_peri('another computer', 'computer')

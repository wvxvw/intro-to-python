# -*- coding: utf-8 -*-

# The requested function used to be a Python's built-in, however, for
# no good reason it was removed from Python 3.  The code that tries to
# be both Python 2 and Python 3 compatible, could use something like
# this:
#
# import sys
#
#
# if sys.version_info[0] < 3:
#     compare = cmp
# else:
#     def compare(a, b):
#         return ((a < b) - (a > b))


def compare(a, b):
    return ((a > b) - (a < b))

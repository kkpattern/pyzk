# Copyright (c) 2012 zhangkai

# Util functions and classes of urllib2 module

import os
import errno

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as e:
        if e.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

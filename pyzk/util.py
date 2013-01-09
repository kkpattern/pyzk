# Copyright (c) 2012 zhangkai

import socket
import sys
import threading
import traceback

def dump_stacks(signal, frame):
    """dump the stacks of all threads in a process.

    Thanks to haridsv and Will on StackOverflow.

    """
    id2name = dict([(th.ident, th.name) for th in threading.enumerate()])
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)"%(id2name.get(threadId,""), threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s'%(filename, lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    print "\n".join(code)
  
def get_local_ip_address(target):
    """get the local ip address used to connect to the target."""
    ipaddr = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((target, 8000))
        ipaddr = s.getsockname()[0]
        s.close()
    except:
        pass
    return ipaddr

class Progress(object):
    """Progress object.

    use += to add progress.
    use str(progress) to get the current progress.

    """
    def __init__(self, current_value=0, max_value=100):
        self.previous_value = 0
        self.current_value = current_value
        self.max_value = max_value

    def __iadd__(self, value):
        self.previous_value = self.current_value
        self.current_value += value
        if self.current_value > self.max_value:
            self.current_value = self.max_value
        return self

    def __isub__(self, value):
        self.previous_value = self.current_value
        self.current_value -= value
        if self.current_value < 0:
            self.current_value = 0
        return self

    def __float__(self):
        return float(self.current_value)/self.max_value

    def __str__(self):
        return "{0:.1f}%".format(float(self)*100)

    def show(self, accuracy=0):
        """Print the progress to the stdout.

        Args:
            accuracy: digits after the decimal point.

        """
        current_progress = round(float(self.current_value*100)/self.max_value,
                                 accuracy)
        previous_progress = round(float(self.previous_value*100)/self.max_value,
                                 accuracy)
        if current_progress > previous_progress:
            print "{0}%".format(current_progress)

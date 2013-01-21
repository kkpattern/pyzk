# Copyright (c) 2012 zhangkai

import datetime
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

class Retry(object):
    """Add retry to target function.

    Args:
        target: target function.
        max_retry: max retry times.
        exception_handler: function(retry_time, exception_object)
                           called when exception is raised by target.

    """
    def __init__(self, target, max_retry, exception_handler):
        self.__target = target
        self.__max_retry = max_retry
        self.__exception_handler = exception_handler

    def __call__(self, *args, **kargs):
        for i in range(self.__max_retry-1):
            try:
                return self.__target(*args, **kargs)
            except Exception as e:
                self.__exception_handler(i, e)
        # NOTE: final shot. raise the exception if somethins is wrong.
        return self.__target(*args, **kargs)

class Progress(object):
    """Progress object.

    use += to add progress.
    use str(progress) to get the current progress.

    """
    def __init__(self, current_value=0, max_value=100, out=None):
        self.previous_value = 0
        self.current_value = current_value
        self.max_value = max_value
        if out:
            self.out = out
        else:
            self.out = sys.stdout
        if hasattr(self.out, "isatty") and self.out.isatty():
            self.carriage = '\r'
        else:
            self.carriage = '\n'

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
            self.out.write("{0}% {1}".format(current_progress, self.carriage))
            self.out.flush()

class TimedProgress(Progress):
    def __init__(self, current_value=0, max_value=100, out=None):
        super(TimedProgress, self).__init__(current_value,
                                            max_value,
                                            out)
        self.started_at = datetime.datetime.now()

    def time_left(self):
        """Time left with accuracy in seconds."""
        progress_now = float(self)
        if progress_now == 0.0:
            return None
        time_passed = datetime.datetime.now()-self.started_at
        time_passed_in_seconds = (
            time_passed.seconds + time_passed.days * 24 * 3600)
        time_left_in_seconds = time_passed_in_seconds*(
            (1-progress_now)/progress_now)
        return datetime.timedelta(seconds=int(time_left_in_seconds))

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
            self.out.write("{0}% {1} left{2}".format(
                current_progress, str(self.time_left()), self.carriage))
            self.out.flush()

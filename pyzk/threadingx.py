# Copyright (c) 2012 zhangkai

# Util functions and classes of threading module

import threading

class StoppableThread(threading.Thread):
    """the same class as the threading.Thread except you can
       call set_stop_signal() to set a stop signal and
       call get_stop_signal() to tell if a stop signal is set."""
    def __init__(self, group=None, target=None,
                 name=None, stop_event=None, args=(), kwargs={}):
        threading.Thread.__init__(self, group, target, name, args, kwargs)
        if stop_event:
            self.__stop_event = stop_event
        else:
            self.__stop_event = threading.Event()

    def set_stop_signal(self):
        self.__stop_event.set()

    def get_stop_signal(self):
        return self.__stop_event.is_set()

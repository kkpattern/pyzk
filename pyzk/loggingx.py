import logging
import logging.handlers

class SingleLevelFilter(logging.Filter):
    """Accept/Reject a single level.

    Thanks to Vinay Sajip, the author of python logging

    """
    def __init__(self, level, accept):
        """initialize a SingleLevelFilter.

        Args:
            level: logging level
            accept: Only accept the single level is accept=True,
                    otherwise only reject the single level
        """
        self.__level = level
        self.__accept = accept

    def filter(self, record):
        # return true means the record is going to be logged
        if self.__accept:
            # accept the single class, so when the record
            # is the required level return true
            return (record.levelno == self.__level)
        else:
            return (record.levelno != self.__level)

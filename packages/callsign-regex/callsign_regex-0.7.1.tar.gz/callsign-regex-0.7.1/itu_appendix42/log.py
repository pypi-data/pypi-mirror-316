""" itu_appendix42 log.py
Copyright (C) 2024 Martin J Levy - W6LHI/G8LHI - @mahtin - https://github.com/mahtin
"""

import logging

class ItuAppendix42Logger():
    """ ItuAppendix42 Logger """

    def __init__(self, debug_level=False):
        """ ItuAppendix42 Logger """
        self._debug_level = self._convert_logging_level(debug_level)
        self._logger = None
        # logging.basicConfig(level=self._debug_level)

    def getLogger(self):
        """ ItuAppendix42 Logger """
        # create logger
        logger = logging.getLogger('ItuAppendix42')
        logger.setLevel(self._debug_level)

        ch = logging.StreamHandler()
        ch.setLevel(self._debug_level)

        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # add formatter to ch
        ch.setFormatter(formatter)

        # add ch to logger
        logger.addHandler(ch)

        self._logger = logger

        return logger

    def _convert_logging_level(self, debug_level):
        """ ItuAppendix42 Logger """
        if debug_level:
            # will display DEBUG, INFO, WARNING, ERROR, CRITICAL
            return logging.DEBUG
        else:
            # will display WARNING, ERROR, CRITICAL
            return logging.WARNING

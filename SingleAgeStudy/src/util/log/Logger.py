# -*- coding: utf-8 -*-

import logging
from logging.handlers import RotatingFileHandler

from util import Constants

## CLass Logger
#  ============
#
# This class Logger is a singleton which allow to log anywhere in the program.
#
# There is different logging's level:
#    - DEBUG: show all possible log.
#    - INFO: show ino tu user but no developper info.
#    - WARNING: show messages about something which can altered the processing.
#    - ERROR: error happened during processing but no able to completely stop
#    the program.
#    - CRITICAL: an error occurred and stop the program.
#
# ERROR and CRITICAL level log also the stacktrace.
#
# By default, the logging mode is set to DEBUG.
#
class Logger(object):

    __instance = None

    ## Constructor of Logger
    #  ---------------------
    #
    # Instance variable:
    #    - logg: a logging object which allow to log.
    def __init__(self, log_path= Constants.PATH_LOG, mode=Constants.MODE_INFO, writting_mode=Constants.LOG_NO_APPEND):
        self.logg = Logger.setLogger( log_path, mode, writting_mode)
        self.mode = mode

    ## setLogger
    #  ---------
    #
    # Defines options to the Logger.
    #
    @staticmethod
    def setLogger( log_path, mode, writting_mode):

        # Reinitialize log file
        ERROR_FILE = open( log_path, "w")
        ERROR_FILE.write("-----------------------------------")
        ERROR_FILE.close()

        # Logger object which is used to write in log
        logger = logging.getLogger()
        # Set level to mode.
        logger.setLevel(mode)

        # Create formatter which will add time and log level for each message
        # when a message will be written
        formatter = logging.Formatter \
        ('%(asctime)s :: %(levelname)s :: %(message)s')

        # Create the handler which will redirect the message to the
        # log file, with append mode, 2 backups and maximum size of
        # 1 Mo
        file_handler = RotatingFileHandler( log_path, 'a', 1000000, 2)
        # Set level on mode
        file_handler.setLevel(mode)
        file_handler.setFormatter(formatter)
        # add this handler to the logger
        logger.addHandler(file_handler)

        # Second handler to print log message on console
        steam_handler = logging.StreamHandler()
        steam_handler.setLevel(mode)
        logger.addHandler(steam_handler)

        return logger

    ## get_instance
    #  ------------
    #
    # First time create an instance of Logger, then return this instance.
    # So after the first instantiation, the next instantiation returns all the
    # same object.
    #
    # @return Logger instance.
    @staticmethod
    def get_instance( log_path= Constants.PATH_LOG, logging_mode=Constants.MODE_INFO, writting_mode=Constants.LOG_APPEND):
        if Logger.__instance == None:
            Logger.__instance = Logger( log_path, logging_mode, writting_mode)
        return Logger.__instance

    ## debug
    #  -----
    #
    # Log debug
    #
    # @param message: messgae to log
    #
    # @return None
    def debug(self, message):
        if self.mode == Constants.MODE_DEBUG:
            self.logg.debug(message)

    ## info
    #  ----
    #
    # Log info
    #
    # @return None
    def info(self, message):
        if (self.mode == Constants.MODE_DEBUG or
            self.mode == Constants.MODE_INFO):
                self.logg.info(message)

    ## warning
    #  -------
    #
    # Log warning
    #
    # @return None
    def warning(self, message):
        if (self.mode == Constants.MODE_DEBUG or
            self.mode == Constants.MODE_INFO or
            self.mode == Constants.MODE_WARNING):
                self.logg.warning(message)

    ## error
    #  -----
    #
    # Log error
    #
    # @return None
    def error(self, message, ex=True):
        if ex == True:
            if (self.mode == Constants.MODE_DEBUG or
                self.mode == Constants.MODE_INFO or
                self.mode == Constants.MODE_WARNING or
                self.mode == Constants.MODE_ERROR):
                    self.logg.error(message, exc_info=True)
        else:
            if (self.mode == Constants.MODE_DEBUG or
                self.mode == Constants.MODE_INFO or
                self.mode == Constants.MODE_WARNING or
                self.mode == Constants.MODE_ERROR):
                    self.logg.error(message)

    ## critical
    #  --------
    #
    # Log critical
    #
    # @return None
    def critical(self, message):
        self.logg.critical(message, exc_info=False)
        exit()
        
    #
    # Close all logging handlers
    #
    # @return None        
    def close(self):
        
        handlers = self.logg.handlers[:]
        for handler in handlers:
            handler.close()
            self.logg.removeHandler(handler)

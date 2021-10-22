# -*- coding: utf-8 -*-

from util.exception.SNPnetException import SNPnetException

## Class FileFormatException
#  =========================
#
# Exception raised in case of file format given in a method is not the
# correct format.
class FileFormatException(SNPnetException):
    ##  Constructor of FileFormatException
    #  -----------------------------------
    #
    #    @param message : a message describing in which context the exception happened.
    def __init__ (self, message):
        super( MeanException, self).__init__( message, "")


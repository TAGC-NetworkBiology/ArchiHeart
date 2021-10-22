# -*- coding: utf-8 -*-

## Class SNPnetException
#  ===============================
#
#  Exception raised in case of a ProcessedPhenotype object's integrity is not
#  respected.
#
class SNPnetException(Exception):
    ##  Constructor of SNPnetException
    #  -----------------------------------------
    #
    #    @param message : a message describing in which context the exception
    #                happened.
    #    @param info : additional info.
    def __init__ (self, message, info=''):
        self.message = message
        self.info = info

    ## get_msg
    #  -------
    #
    # Return the message.
    #
    # @return String
    def get_msg(self):
        return self.message

    ## print_error
    #  ----------
    #
    #  Return a string explaining the exception.
    # The string is the message given when the exception is raised.
    #
    # @return String
    def print_error(self):
        string = "\n\n---------------------------------------------------------------------------\n"
        string = string + self.message + str(self.info)
        string = string + "\n---------------------------------------------------------------------------\n\n"
        return string

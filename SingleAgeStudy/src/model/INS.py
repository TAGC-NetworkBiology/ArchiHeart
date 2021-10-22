# -*- coding: utf-8 -*-

from Mutation import Mutation
from util import Constants

## Class INS
#  =========
#
# Each instance of this class represent an INSertion (inherited from Mutation).
# Each object INS contains :
class INS(Mutation):
    __mapper_args__ = { 'polymorphic_identity':'INS' }

    def __str__(self):
        string = Constants.DGRP_ENTRY_INSERTION_TAG + " : " + self.mutation_id + "\nPosition : " + self.position + "\nChrom :  " + self.chromosom + "\nRef count : " + str(self.refCount) + "\nAlt count : " + str(self.altCount)
        return string


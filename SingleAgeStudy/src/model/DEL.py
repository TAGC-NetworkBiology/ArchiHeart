# -*- coding: utf-8 -*-

from Mutation import Mutation
from util import Constants

## Class DEL
#  =========
#
# Each instance of this class represent a DELetion (inherited from Mutation).
# Each object DEL contains :
class DEL(Mutation):
    __mapper_args__ = {'polymorphic_identity':'DEL' }

    def __str__(self):
        string = Constants.DGRP_ENTRY_DELETION_TAG + " : " + self.mutation_id + "\nPosition : " + self.position + "\nChrom :  " + self.chromosom + "\nRef count : " + str(self.refCount) + "\nAlt count : " + str(self.altCount)
        return string


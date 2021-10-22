# -*- coding: utf-8 -*-


from Mutation import Mutation
from util import Constants


## Class MNP
#  =========
#
# Each instance of this class represent an Multiple Nucleotide Polymorphism
# (inherited from Mutation).
# Each object MNP contains :
class MNP(Mutation):
    __mapper_args__ = { 'polymorphic_identity':'MNP' }

    def __str__(self):
        string = Constants.DGRP_ENTRY_MNP_TAG + " : " + self.mutation_id + "\nPosition : " + self.position + "\nChrom :  " + self.chromosom + "\nRef count : " + str(self.refCount) + "\nAlt count : " + str(self.altCount)
        return string


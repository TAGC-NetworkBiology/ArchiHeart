# -*- coding: utf-8 -*-

from Mutation import Mutation
from util import Constants

## Class SNP
#  =========
#
# Each instance of this class represent an Single Nucleotide Polymorphism
# (inherited from Mutation).
# Each object SNP contains :
class SNP(Mutation):
    __mapper_args__ = {'polymorphic_identity':'SNP' }

    # Print a string describing a SNP
    def __str__(self):
        string = Constants.DGRP_ENTRY_SNP_TAG + " : " + self.mutation_id + "\nPosition : " + self.position + "\nChrom :  " + self.chromosom + "\nRef count : " + str(self.refCount) + "\nAlt count : " + str(self.altCount)
        return string


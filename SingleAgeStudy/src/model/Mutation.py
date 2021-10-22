# -*- coding: utf-8 -*-



import abc

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from util.sql.Base import Base
from model.AssociationMutationLine import AssociationMutationLine
from model.ProcessedMutation import ProcessedMutation
from model.MutationEffect import MutationEffect

## Class Mutation
#  ==============
#
# Each instance of this class is a Mutation present in the VCF file DGRP.
# Each Mutation contains:
#     - mutation_id: (String) the Mutation's id.
#     - position: (String) indicating the position of the Mutation on the
#                 chromosom.
#     - chromosom: (String) the chromosom's name where the Mutation appears.
#     - refCount: (Integer) tells how many times this mutation is in its
#                 reference form
#     - altCount: (Integer) tells how many times this mutation is in its
#                 alternative form
#     - reference lines : what D.melanogaster lines contain the reference allele
#     - alternative lines : what D.melanogaster lines contain the mutation allele.
#    - refAll: (String) the reference allele.
#    - altAll: (String) the alternative allele.
#    - type_mutation: (String) the mutation's type among ('INS', 'DEL', 'SNP',
#                       'MNP')
#    - altLineList: list<Line> list of Line objects where the considered
#                    Mutation is present.
#    - mutation_effectList: list<MutationEffect> list all effects for this
#                            Mutation
#    - processed_mutation_list: list<ProcessedMutation> list of
#                         ProcessedMutation corresponding to the different
#                         phenotype analyzed.
class Mutation(Base):
    __metaclass = abc.ABCMeta
    __tablename__ = 'mutation'

    mutation_id = Column(String, primary_key=True)
    position = Column(String)
    chromosom = Column(String)
    refCount = Column(Integer)
    altCount = Column(Integer)
    refAll = Column(String)
    altAll = Column(String)
    type_mutation = Column(String)
    altLineList = relationship('Line', secondary='mutation_in_line', backref='mutations')
    mutation_effectList = relationship('MutationEffect', backref='mutation')

    __mapper_args__ = {'polymorphic_identity': 'mutation',
                       'polymorphic_on': type_mutation}

    ## get_mutation_id
    #  ---------------
    #
    # Return the mutation_id.
    #
    # @return String
    def get_mutation_id(self):
        return self.mutation_id


    ## get_ref_count
    #  -------------
    #
    # Return the count of Line objects with the reference allele.
    #
    # @return Integer
    def get_ref_count(self):
        return self.refCount

    ## get_alt_count
    #  -------------
    #
    # Return the count of Line objects with the alternative allele.
    #
    # @return  Integer
    def get_alt_count(self):
        return self.altCount

    ## get_alt_line_list
    #  -----------------
    #
    # Return the alternative line list.
    #
    # @return  List<Line>
    def get_alt_line_list(self):
        return self.altLineList

    ## get_mutation_effect_list
    #  ------------------------
    #
    # Return the mutation_effect list.
    #
    # @return  List<MutationEffect>
    def get_mutation_effect_list(self):
        return self.mutation_effectList


    ## add_mutation_effect
    #  -------------------
    #
    # Add object Effect to mutation_effectList.
    #
    # @param mutation_effect: MutationEffect to add to the current Mutation
    #
    # @return None
    def add_mutation_effect(self, mutation_effect):
        self.mutation_effectList.append(mutation_effect)
        return

    ## add_alt_line
    #  ------------
    #
    # Append 'line' to altLineList if 'line' is not None.
    #
    # @param line: Line object to add to the altLineList.
    #
    # @return None
    def add_alt_line(self, line):
        if line != None:
            self.altLineList.append(line)
        return


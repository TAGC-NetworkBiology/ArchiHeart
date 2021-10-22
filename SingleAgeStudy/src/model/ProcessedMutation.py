# -*- coding: utf-8 -*-

import time

from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from sqlalchemy.sql.schema import Index, ForeignKeyConstraint

from util.sql.Base import Base
from model.ProcessedStrain import ProcessedStrain
from __builtin__ import int


## Class ProcessedMutation
#  =======================
#
# Each instance of ProcessedMutation is a ProcessedMutation object.
# A ProcessedMutation object represents a treated Mutation: a weight is
# computed and assigned to the studied Mutation objects as well as a rank.
#
# The ProcessedMutation object with the lower rank and the highest weight is
# the most probably responsible for the studied phenotype (ProcessedPhenotype),
# in the strains (ProcessedStrain) where this mutation is expressed.
#
# Each ProcessedMutation object contains:
#    - id: (Integer) autoincremented identifier.
#    - phenotype_name: (String) the studied phenotype's name.
#    - name: (String) the processed mutation's name. (Mutation.mutation_id)
#    - rank: (Integer) rank of this processed mutation.
#    - weight: (Float) the computed weight.
#    - ratio: (Float) the ratio representing the proportion of mutations with
#            an higher or lower weight.
#    - mutation: (Mutation) associated.
#    - number_line: (Integer)number of strain where the alternative allele's
#            ProcessedMutation is present.
#
#    - phenotype: (ProcessedPhenotype) associated. (only in objec)
#
#
class ProcessedMutation(Base):

    __tablename__ = 'processed_mutation'

    phenotype_name = Column(String)
    method = Column(String)
    age = Column(Integer)
    name = Column(String, ForeignKey('mutation.mutation_id'))
    number_line = Column(Integer)
    rank = Column(Integer)
    weight = Column(Float)
    ratio = Column(Float)
    fdr = Column( Float)
    # phenotype = created by backref in ProcessedPhenotype.py

#     index_processed_mutation = Index(name, phenotype_name, weight, rank)
    __table_args__ = (ForeignKeyConstraint([phenotype_name, method, age],
                                           ['processed_phenotype.name', 'processed_phenotype.method', 'processed_phenotype.age']),
                      PrimaryKeyConstraint( 'phenotype_name', 'method', 'age', 'name'),
                      {})

    ## set_number_line
    #  ---------------
    #
    # @param n: number of lines. (Integer)
    #
    # @return nothing.
    def set_number_line(self, n):
        self.number_line = n
        return

    ## set_ratio
    #  ---------
    #
    # Set the ratio corresponding to the proportion or weight higher/equal (for
    # positive weights) or  lower/equal ( for negatives weights) than the self
    # ProcessedMutation's weight.
    #
    # @param ratio: Float
    def set_ratio(self, ratio):
        self.ratio = ratio
        return

    ## get_ratio
    #  ---------
    #
    # Return the ratio associated to this ProcessedMutation
    #
    # @return Float
    def get_ratio(self):
        return self.ratio

    ## get_number_lines
    #  ----------------
    #
    # @return
    def get_number_lines(self):
        return self.number_line

    ## get_age
    #  -------
    #
    # Return the age
    #
    # @return Integer
    def get_age(self):
        return self.age

    ## get_name
    #  --------
    #
    # Return self.name : the mutation_id
    #
    # @return String
    def get_name(self):
        return self.name

    ## get_phenotype_name
    #  ------------------
    #
    # Return self.phenotype_name : the phenotype_name.
    #
    # @return String
    def get_phenotype_name(self):
        return self.phenotype_name

    ## get_weight
    #  ----------
    #
    # Return self.weight.
    #
    # @return Float
    def get_weight(self):
        return self.weight

    ## get_rank
    #  ----------
    #
    # Return self.rank.
    #
    # @return Integer
    def get_rank(self):
        return self.rank

    ## set_weight
    #  ----------
    #
    # Set 'weight' to self.weight variable.
    #
    # @param weight : float
    #
    # @return None
    def set_weight(self, weight):
        if type(weight) == float:
            self.weight = weight
        return

    ## set_rank
    #  --------
    #
    # Assign value 'rank' to self.rank.
    #
    # @param rank: Integer value to set to self.rank
    #
    # @return Boolean
    def set_rank(self, rank):
        if type(rank) != int:
            return False

        self.rank = rank
        return True

    ## compute_weight
    #  --------------
    #
    # Compute weight for the current ProcessedMutation.
    #
    #    @param processed_strain_list : list<ProcessedStrain>
    #    where the mutation is present.
    #
    # Return the mutation_weight.
    #
    # @return Float
    @staticmethod
    def compute_weight(processed_strain_list):
        temporary_result = 0.0

        for strain in processed_strain_list:
            if strain.get_type() == 'LOW':
                temporary_result += -1 * (strain.get_reference_value() * strain.get_rank())
            elif strain.get_type() == 'HIGH':
                temporary_result += strain.get_reference_value() * strain.get_rank()

        # Compute the mutation_weight : float value allow to rank mutations.
        mutation_weight = float(temporary_result) / float(len(processed_strain_list))

        return mutation_weight

# -*- coding: utf-8 -*-


from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import PrimaryKeyConstraint, ForeignKeyConstraint

from util.sql.Base import Base
from operator import attrgetter, methodcaller
from util.exception.ProcessedPhenotypeException import ProcessedPhenotypeException
from model.AnalyzedGene import AnalyzedGene


## Class AnalyzedPhenotype
#  ======================
#
# Each instance of this class is an analyzed phenotype.
# An analyzed phenotype has a name (exemple : 'Heartrate_Mean'), a method to study
# its data ( among : 'mean', 'IQR', '1.5IQR'), a ProcessedPhenotype (pre-processed phenotype data),
# a list of AnalyzedMutation (mutation considered as significant for this analysis) and
# a list of AnalyzedGene (genes that carry at least one significant mutation).
#
# This class has a 1-to-many relationship with ProcessedPhenotype
class AnalyzedPhenotype(Base):
    __tablename__ = 'analyzed_phenotype'

    ## @b Variables @b of @b ProcessedPhenotype:
    #
    #     - name: phenotype's name (e.g 'Heartperiod_Mean')
    #     - method: method to use to analyze phenotype with the data. (e.g 'IQR')
    #     - age: the age of the fly
    #     - alpha : the threshold for p-value on mutations (first-order risk)
    #     - analyzed_mutation_list: list<AnalyzedMutation>
    #     - analyzed_gene_list: list<AnalyzedGene>
    name = Column(String)
    age = Column(Integer)
    alpha = Column( Float)
    method = Column(String)
#     analyzed_mutation_list = relationship('AnalyzedMutation', backref='analyzed_phenotype', cascade='all, delete-orphan')
    analyzed_gene_list = relationship('AnalyzedGene', backref='analyzed_phenotype', cascade='all, delete-orphan')

    __table_args__ = (
        PrimaryKeyConstraint('name', 'method', 'age', 'alpha'),
        ForeignKeyConstraint([name, method, age],
                    ['processed_phenotype.name', 'processed_phenotype.method', 'processed_phenotype.age']),
                      {}
    )


    ## add_gene
    #  --------
    #
    # Add AnalyzedGene to AnalyzedPhenotype
    #
    def add_gene(self, gene):
        if isinstance(gene, AnalyzedGene) == False:
            raise AnalyzedPhenotypeException('"gene" can not be added '
                                            'to AnalyzedPhenotype object,'
                                            ' "gene" is not an instance of'
                                            'AnalyzedGene: '\
                                            , gene)
        self.analyzed_gene_list.append(gene)
        return

#     ## add_mutation
#     #  ------------
#     #
#     # Add AnalyzedMutation to analyzed_mutation_list.
#     #
#     # @param mutation: AnalyzedMutation object to add to the AnalyzedPhenotype
#     #
#     # @return None
#     def add_mutation(self, analyzed_mutation):
#         try:
#             analyzed_mutation
#         except NameError:
#             raise AnalyzedPhenotypeException('"analyzed_mutation" can not be'
#                         ' added to AnalyzedPhenotype object.')
#         # Test if mutation is a AnalyzedMutation object.
#         if isinstance(analyzed_mutation, AnalyzedMutation) == False:
#             raise AnalyzedPhenotypeException('"analyzed_mutation" can not be'
#                                     ' added to AnalyzedPhenotype object, mutation'
#                                     ' is not an instance of AnalyzedMutation: '\
#                                     , analyzed_mutation)
# 
#         self.analyzed_mutation_list.append( analyzed_mutation)
# 
#         return



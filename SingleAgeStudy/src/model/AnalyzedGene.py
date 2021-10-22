# -*- coding: utf-8 -*-


from util.sql.Base import Base
from sqlalchemy import Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from sqlalchemy.sql.schema import Index, ForeignKeyConstraint

from model.AnalyzedMutation import AnalyzedMutation


class AnalyzedGene(Base):
    __tablename__ = 'analyzed_gene'

    analyzed_phenotype_name = Column(String)
    age = Column(String)    
    method = Column(String)
    alpha = Column( Float)
    category = Column(String)
    flybase_id = Column(String)
    symbol = Column(String)
    best_rank = Column(Integer)
    line_number = Column(Integer)
    significative_mutation = Column(Integer)
    GWAS = Column(Boolean)
    RNAi = Column(Boolean)
    
    analyzed_mutation_list = relationship('AnalyzedMutation', backref='analyzed_gene', cascade='all, delete-orphan')
    # phenotype = Created by relationship one to many in ProcessedPhenotype

#     index_analyzed_gene = Index(age, processed_phenotype_name, category, method)
    __table_args__ = (
        PrimaryKeyConstraint('analyzed_phenotype_name', 'method', 'age', 'category', 'flybase_id', 'alpha'),
        ForeignKeyConstraint([age, method, analyzed_phenotype_name, alpha],
                            ['analyzed_phenotype.age', 'analyzed_phenotype.method', 'analyzed_phenotype.name', 'analyzed_phenotype.alpha']),
                      {}
                      )

    ## add_mutation
    #  ------------
    #
    # Add AnalyzedMutation to analyzed_mutation_list.
    #
    # @param mutation: AnalyzedMutation object to add to the AnalyzedPhenotype
    #
    # @return None
    def add_mutation(self, analyzed_mutation):
        try:
            analyzed_mutation
        except NameError:
            raise AnalyzedPhenotypeException('"analyzed_mutation" can not be'
                        ' added to ProcessedPhenotype object.')
        # Test if mutation is a AnalyzedMutation object.
        if isinstance(analyzed_mutation, AnalyzedMutation) == False:
            raise AnalyzedPhenotypeException('"analyzed_mutation" can not be'
                                    ' added to AnalyzededPhenotype object, mutation'
                                    ' is not an instance of AnalyzedMutation: '\
                                    , analyzed_mutation)

        self.analyzed_mutation_list.append( analyzed_mutation)

        return
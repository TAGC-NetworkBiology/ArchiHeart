# -*- coding: utf-8 -*-


from util.sql.Base import Base
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Float
from sqlalchemy.sql.schema import Index, ForeignKeyConstraint


##
# This class describe a mutation that was considered as significant by the analysis
# 
class AnalyzedMutation(Base):
    __tablename__ = 'analyzed_mutation'

    analyzed_phenotype_name = Column(String)
    analyzed_gene_fbid = Column( String) 
    age = Column(Integer)
    method = Column(String)
    category = Column(String)
    alpha = Column( Float)
    name = Column(String, ForeignKey('mutation.mutation_id'))
    rank = Column(Integer)
    weight = Column(Float)
    ratio = Column(Float)
    number_line = Column(Integer)

#     index_processed_mutation = Index(name, phenotype_name, weight, rank)
    __table_args__ = (
        PrimaryKeyConstraint('analyzed_phenotype_name', 'method', 'age', 'category', 'alpha', 'name'),
        ForeignKeyConstraint([age, method, analyzed_phenotype_name,
                               alpha, category, analyzed_gene_fbid],
                            ['analyzed_gene.age', 'analyzed_gene.method', 'analyzed_gene.analyzed_phenotype_name',
                              'analyzed_gene.alpha', 'analyzed_gene.category', 'analyzed_gene.flybase_id']),
                      {}
                      )

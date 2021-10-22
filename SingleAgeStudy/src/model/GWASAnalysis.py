# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Boolean, Integer, Float
from sqlalchemy.orm import relationship

from util.sql.Base import Base
from model.GWASPhenotypeValue import GWASPhenotypeValue
from model.GWASCovariableValue import GWASCovariableValue
from model.GWASIdentifiedSNP import GWASIdentifiedSNP

## Class GWASAnalysis
#  ============
#
# Each instance of the class GWASAnalysis represent an execution of a GWAS analysis on DGRP phenotype data
#
# A  GWAS Analysis object has:
#    - an id that is autoincremental
#    - a phenotype name corresponding to the phenotype tested in the GWAS
#    - an age corresponding to the age of the DGRP strains analyzed
#    - a correction mode corresponding to the type of correction applied to the list of individual phenotype data on each strain
#    - a transformation mode corresponding to the type of modification applied to the list of means of phenotype values of each strains when outliers are detected
#    - a list of associated values corresponding to the strain and phenotype values used

class GWASAnalysis(Base):
    __tablename__ = 'gwas_analysis'

    gwas_id = Column( Integer, primary_key=True, autoincrement=True)
    phenotype_name = Column( String)
    age = Column( Integer)
    correction_mode = Column( String)
    transformation_mode = Column( String)
    genotype = Column( String)
    covariable = Column( String)
    alpha = Column( Float)
    phenotype_values_list = relationship('GWASPhenotypeValue', backref='associated_gwasanalysis', cascade='all, delete-orphan')
    covariable_list = relationship('GWASCovariableValue', backref='associated_gwasanalysis', cascade='all, delete-orphan')
    identified_snp_list = relationship('GWASIdentifiedSNP', backref='associated_gwasanalysis', cascade='all, delete-orphan')

    ## get_phenotype_values_list
    #  -------------------
    #
    # Return the list of phenotype values associated to this GWAS analysis.
    #
    # @return list<GWASPhenotypeValue>
    def get_phenotype_values_list(self):
        return self.phenotype_values_list

    ## add_phenotype_value
    #  -------------
    #
    # Append to instance variable phenotype_values_list one instance of object of type GWASPhenotypeValue
    #
    #    @param value : object of type GWASPhenotypeValue
    #
    # @return None
    def add_phenotype_value(self, value):
        if isinstance( value, GWASPhenotypeValue):
            self.phenotype_values_list.append( value)
        return
    

    ## add_covariable_value
    #  -------------
    #
    # Append to instance variable covariable_list one instance of object of type GWASCovariableValue
    #
    #    @param value : object of type GWASCovariableValue
    #
    # @return None
    def add_covariable(self, value):
        if isinstance( value, GWASCovariableValue):
            self.covariable_list.append( value)
        return
    
    ## add_identified_snp
    #  -------------
    #
    # Append to instance variable identified_snp_list one instance of object of type GWASIdentifiedSNP
    #
    #    @param value : object of type GWASIdentifiedSNP
    #
    # @return None
    def add_identified_snp(self, snp):
        if isinstance( snp, GWASIdentifiedSNP):
            self.identified_snp_list.append( snp)
        return


    def __eq__(self, other):
        return self.id == other.id

    def __str__(self):
        string = self.id
        return string

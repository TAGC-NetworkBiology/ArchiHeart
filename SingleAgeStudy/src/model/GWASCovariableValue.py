# -*- coding: utf-8 -*-


from model.PhenotypeData import PhenotypeData

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from util.sql.Base import Base


## Class GWASCovariableValue
#  =========================
#
# Each instance of object GWASCovariableValue represents a covairable value associated to a strain and used in a GWAS analysis 
# An GWASCovariableValue object own :
#    - associated_gwasanalysis: The id of the GWAS analysis it is associated with
#    - a strain_number corresponding to the strain having this value
#    - a covariable_name corresponding to the associated corvariable name
#    - a covariable_value corresponding to the associated corvariable value
class GWASCovariableValue(Base):
    __tablename__ = 'gwas_covariable_value'

    # associated_gwasanalysis = variable created by the backref in 'GWASAnalysis'
    associated_gwasanalysis_id = Column( Integer, ForeignKey('gwas_analysis.gwas_id'), primary_key=True)
    strain_number = Column( String, primary_key=True)
    covariable_name = Column( String, primary_key=True)
    covariable_value = Column( String)
    

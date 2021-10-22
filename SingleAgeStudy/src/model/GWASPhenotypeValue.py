# -*- coding: utf-8 -*-


from model.PhenotypeData import PhenotypeData

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from util.sql.Base import Base


## Class GWASPhenotypeValue
#  =========================
#
# Each instance of object GWASPhenotypeValue represents a strain phenotype value used ina a GWAS analysis 
# An GWASPhenotypeValue object own :
#    - associated_gwasanalysis: The id of the GWAS analysis it is associated with
#    - a strain_number corresponding to the strain having this value
#    - a phenotype_value corresponding to the associated phenotype value
class GWASPhenotypeValue(Base):
    __tablename__ = 'gwas_phenotype_value'

    # associated_gwasanalysis = variable created by the backref in 'GWASAnalysis'
    associated_gwasanalysis_id = Column( Integer, ForeignKey('gwas_analysis.gwas_id'), primary_key=True)
    strain_number = Column( String, primary_key=True)
    phenotype_value = Column( Float)
    

# -*- coding: utf-8 -*-


from model.PhenotypeData import PhenotypeData

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from util.sql.Base import Base


## Class GWASIdentifiedSNP
#  =========================
#
# Each instance of object GWASIdentifiedSNP represents a SNP detected by the GWAS analysis as significant for the phenotype 
# An GWASIdentifiedSNP object own :
#    - associated_gwasanalysis: The id of the GWAS analysis it is associated with
#    - a snp_id corresponding to the identifier of the SNP
#    - a chromosome corresponding to the chromosome of the SNP
#    - a position corresponding to the SNP position on its chromosome
#    - a pvalue corresponding to the p-value computed by the GWAS analysis for this SNP
#    - a snp_weight
#    - a snp_weight_se
#    - a snp_fract_var_expl corresponding to the fraction of variability explained by the SNP
#    - a mixing
#    - a nullh2
class GWASIdentifiedSNP(Base):
    __tablename__ = 'gwas_identified_snp'

    # associated_gwasanalysis = variable created by the backref in 'GWASAnalysis'
    associated_gwasanalysis_id = Column( Integer, ForeignKey('gwas_analysis.gwas_id'), primary_key=True)
    snp_id = Column( String, primary_key=True)
    chromosome = Column( String)
    position = Column( Integer)
    pvalue = Column( Float)
    snp_weight = Column( Float)
    snp_weight_se = Column( Float)
    snp_fract_var_expl = Column( Float)
    mixing = Column( Float)
    nullh2 = Column( Float)
    

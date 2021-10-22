# -*- coding: utf-8 -*-

from sqlalchemy import Column, Float, Integer, String, ForeignKey

from util.sql.Base import Base
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from sqlalchemy.sql.schema import Index, ForeignKeyConstraint

## Class ProcessedStrain
#  =====================
#
# Each instance of ProcessedStrain is an object ProcessedStrain.
# A ProcessedStrain represents a studied strains in a particular context
# (phenotype, method).
#
# A rank is assigned to a ProcessedStrain in funciton of its reference value.
# This reference value is computed with one method among three. (IQR mean ,
# mean, 1,5 IQR mean).
#
# Each ProcessedSrain contains:
#    - id: (Integer) autoincremented identifier.
#    - phenotype_name: (String) phenotype name for this strain.
#    - strain_number: (String) the ProcessedStrain's Strain's strain number.
#    - reference_value: (Float) the ProcessedStrain's reference value.
#    - rank: (Integer) the ProcessedStrain's rank.
#    - phenotype: (ProcessedPhenotype) the phenotype considered.
#    - strain: (Strain) the associated Strain.
#    - method: (String) the method to compute reference value.
class ProcessedStrain(Base):
    __tablename__ = 'processed_strain'
    
    phenotype_name = Column(String)
    method = Column(String)
    age = Column(Integer)
    strain_number = Column(String, ForeignKey('strain.number'))
    reference_value = Column(Float)
    rank = Column(Integer)
    type = Column(String)
    # phenotype = created by backref in ProcessedPhenotype.py (one-to-many)
    # strain = created by backref in Strain.py (one-to-many)

    __table_args__ = (ForeignKeyConstraint([phenotype_name, method, age],
                                       ['processed_phenotype.name', 'processed_phenotype.method', 'processed_phenotype.age']),
                      PrimaryKeyConstraint( 'phenotype_name', 'method', 'age', 'strain_number' ))


#     index_processed_strain = Index(phenotype_name, strain_number, type)

    ## get_age
    #  -------
    #
    # Return the age
    #
    # @return Integer
    def get_age(self):
        return self.age

    ## get_type
    #  --------
    #
    # Return the strain's type.
    #
    # @return String
    def get_type(self):
        return self.type

    ## get_phenotype_name
    #  ------------------
    #
    # Return the phenotype's name.
    #
    # @return String
    def get_phenotype_name(self):
        return self.get_phenotype().get_name()

    ## get_phenotype
    #  -------------
    #
    # Return the associated phenotype.
    #
    # @return ProcessedPhenotype
    def get_phenotype(self):
        return self.phenotype

    ## get_strain_number
    #  -----------------
    #
    # Return self.strain_number.
    #
    # @return String
    def get_strain_number(self):
        return self.strain_number

    ## get_strain
    #  ----------
    #
    # Return the associated strain.
    #
    # @return Strain
    def get_strain(self):
        return self.strain

    ## get_rank
    #  --------
    #
    # Return self.rank
    #
    # @return Integer
    def get_rank(self):
        return self.rank

    ## get_method
    #  ----------
    #
    # Return the method the strain was computed with.
    #
    # @return String
    def get_method(self):
        return self.method

    ## get_reference_value
    #  -----------------------
    #
    # Return self.reference_value
    #
    # @return Float
    def get_reference_value(self):
        return self.reference_value

    ## set_reference_value
    #  -------------------
    #
    #    @param value : float number.
    #
    # Assign reference_value to ProcessedStrain object.
    #
    # @return None
    def set_reference_value(self, value):
        self.reference_value = value
        return

    ## set_type
    #  --------
    #
    #    @param type : string 'LOW' or 'HIGH'.
    #
    # Assign type to ProcessedStrain object.
    #
    # @return None
    def set_type(self, type):
        self.type = type
        return

    ## assign_rank
    #  -----------
    #
    #    @param rank: integer number which corresponds to the ProcessedStrain rank.
    #
    # Assign rank to ProcessedStrain object.
    #
    # @return None
    def assign_rank(self, rank):
        self.rank = rank
        return

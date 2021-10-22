# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.sql.schema import PrimaryKeyConstraint
from sqlalchemy.sql.schema import Index, ForeignKeyConstraint, ForeignKey

from util.sql.Base import Base

## Class ProcessedPhenotypeData
#  ============================
#
# Each instance of this class is a ProcessedPhenotypeData object.
# A ProcessedPhenotypeData represents a data issued from the phenotypic data
# file treated (normalized, centered...)
#
# Each ProcessedPhenotypeData contains:
#    - data_id: (Integer) autoincremented identifier.
#    - phenotype_name: (String) tells the phenotype considered.
#    - individual_name: (String) tells the individual name owning this data.
#    - original_value: original data value.
#    - normalized_value: normalized value.
#    - normalized_centered_value: normalized centered value.
#    - phenotype_data: PhenotypeData related to this ProcessedPhenotypeData.
#    - phenotype: ProcessedPhenotype related to this ProcessedPhenotypeData.
class ProcessedPhenotypeData(Base):
    __tablename__ = 'processed_phenotype_data'

    phenotype_name = Column(String)
    age = Column(Integer)
    individual_name = Column(String)
    original_value = Column(Float)
    normalized_value = Column(Float)
    normalized_centered_value = Column(Float)
    phenotype_data_id = Column(Integer, ForeignKey('phenotype_data.id'))
    # phenotype_data = created by the one-to-many relationship with PhenotypeData.py
    # phenotype = created by backref in ProcessedPhenotype.py

#     index_processed_data = Index(normalized_centered_value, individual_name, phenotype_name)
    __table_args__ = (ForeignKeyConstraint(['phenotype_name', 'age'],
                                           ['processed_phenotype.name', 'processed_phenotype.age']),
                      PrimaryKeyConstraint( 'phenotype_name', 'age', 'individual_name' ))

    ## get_age
    #  -------
    #
    # Return the age.
    #
    # @return Integer
    def get_age(self):
        return self.age

    ## get_individual_name
    #  ------------------
    #
    # Return the associated individual name.
    #
    # @return String
    def get_individual_name(self):
        return self.get_data().get_individual().get_name()

    ## get_data
    #  --------
    #
    # Return self.phenotype_data
    #
    # @return PhenotypeData
    def get_data(self):
        return self.phenotype_data

    ## get_original_value
    #  ------------------
    #
    # Return self.original_value
    #
    # @return Float
    def get_original_value(self):
        return self.original_value


    ## get_normalized_value
    #  ------------------
    #
    # Return self.normalized_value
    #
    # @return Float
    def get_normalized_value(self):
        return self.normalized_value


    ## get_normalized_centered_value
    #  ------------------
    #
    # Return self.normalized_centered_value
    #
    # @return Float
    def get_normalized_centered_value(self):
        return self.normalized_centered_value

    ## add_normalized_centered_value
    #  -----------------------------
    #
    #  Set value (float) to normalized_centered_value.
    #
    # @param value: float
    #
    # @return Boolean
    def set_normalized_centered_value(self, value):
        try:
            value
        except NameError:
            return False

        # Test if value is a float object.
        if type(value) != float:
            if value == 'set_to_none':
                self.normalized_centered_value = None
                return True

            return False

        self.normalized_centered_value = value

        return True

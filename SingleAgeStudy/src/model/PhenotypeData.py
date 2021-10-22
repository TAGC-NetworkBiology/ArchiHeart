# -*- coding: utf-8 -*-

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from util.sql.Base import Base
from model.ProcessedPhenotypeData import ProcessedPhenotypeData
from util.exception.PhenotypeDataException import PhenotypeDataException



## Class PhenotypeData
#  ===================
#
# Each instance of this class represent a PhenotypeData object.
#
# A PhenotypeData object represents the value observed for
# one phenotype and for one individu. The value is untreated. (original value)
#
# Each PhenotypeData contains:
#    - id: (Integer) autoincremented identifier.
#    - phenotype_name: (String) phenotype name ( context for this data)
#    - value: (Float) value observed for one phenotype (ProcessedPhenotype), for one individual (Individual)
#    - individual_name: (String) Individual 's name
#    - processed_data: (ProcessedPhenotypeData) Processed data related to this PhenotypeData.
#    - individual_associated: (Individual) related Individual.
class PhenotypeData(Base):
    __tablename__ = 'phenotype_data'

    id = Column(Integer, primary_key=True, autoincrement=True)
    phenotype_name = Column(String)
    value = Column(Float)
    age = Column(Integer)
    individual_name = Column(String, ForeignKey('individual.name'))
    processed_data = relationship('ProcessedPhenotypeData', backref='phenotype_data')
    # individual_associated = variable created by the backref in 'Individual'

    ## get_name
    #  --------
    #
    # Return the phenotype name (String)
    #
    # @return String
    def get_phenotype_name(self):
        return self.phenotype_name

    ## get_value
    #  ---------
    #
    # Return the value (Float)
    #
    # @return Float
    def get_value(self):
        return self.value

    ## get_age
    #  -------
    #
    # Return the age.
    #
    # @return Integer
    def get_age(self):
        return self.age

    ## get_individual
    #  --------------
    #
    # Return the individual associated to this data.
    #
    # @return Individual
    def get_individual(self):
        return self.individual_associated

    ## add_processed_data
    #  ------------------
    #
    # Add one ProcessedPhenotypeData object to processed_data.
    #
    # @param data: ProcessedPhenotypeData to add to the PhenotypeData
    #
    # @return None
    def add_processed_data(self, processed_data):
        try:
            processed_data
        except NameError:
            raise PhenotypeDataException('"processed_data" can not be added '
                                            'to PhenotypeData object.')

        # Test if data is a ProcessedPhenotypeData object.
        if isinstance(processed_data, ProcessedPhenotypeData) == False:
            raise PhenotypeDataException('"processed_data" can not be added '
                                            'to PhenotypeData object,'
                                            ' data is not an instance of'
                                            'ProcessedPhenotypeData: '\
                                            , processed_data)

        self.processed_data.append(processed_data)

        return

    def __str__(self):
        if self.value != None:
            string = self.individual_name + "\t" + self.age + "\t" + self.phenotype_name + "\t" + str(self.value)
        else:
            string = self.individual_name + "\t" + self.age + "\t" + self.phenotype_name + "\tNaN"
        return string

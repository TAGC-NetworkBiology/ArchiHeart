# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship

from util.sql.Base import Base
from model.Individual import Individual
from model.ProcessedStrain import ProcessedStrain

## Class Strain
#  ============
#
# Each instance of the class Strai is a Strain object.
# A Strain object represents a strain present in the data phenotypic file.
#
# A  Strain object has:
#    - control: (Boolean) True if control, False if not.
#    - number: (String) the strain number
#    - list_individual: (List<Individual>) list of Individual in this Strain.
#    - processed_strain_list: (List<processed_strain_list>) list of
#                             ProcessedStrain in this Strain.
class Strain(Base):
    __tablename__ = 'strain'

    control = Column(Boolean)
    number = Column(String, primary_key=True)
    list_individual = relationship('Individual', backref='strain_associated', cascade='all, delete-orphan')
    processed_strain_list = relationship('ProcessedStrain', backref='strain')



    ## get_list_individual
    #  -------------------
    #
    # Return the list of Individual in this Strain.
    #
    # @return list<Individual>
    def get_list_individual(self):
        return self.list_individual

    ## add_processed_strain
    #  --------------------
    #
    # Append a new ProcessedStrain object to processed_strain_list.
    #
    #    @param processed_strain : ProcessedStrain object.
    #
    # @return None
    def add_processed_strain(self, processed_strain):
        self.processed_strain_list.append(processed_strain)
        return

    ## add_individual
    #  -------------
    #
    # Append to instance variable list_individual one instance of object of type Individual
    #
    #    @param individual : object of type Individual
    #
    # @return None
    def add_individual(self, individual):
        if isinstance(individual, Individual):
            self.list_individual.append(individual)
        return

    ## get_control
    #  ------------
    #
    # Return control.
    #
    # @return Boolean
    def get_control(self):
        return self.control

    ## get_number
    #  ----------
    #
    # Return the number.
    #
    # @return String
    def get_number(self):
        return self.number

    ## get_processed_strain_list
    #  -------------------------
    #
    # Return the processed strain list.
    #
    # @return List<ProcessedStrain>
    def get_processed_strain_list(self):
        return self.processed_strain_list


    def __eq__(self, other):
        return self.number == other.number

    def __str__(self):
        string = self.number
        return string

# -*- coding: utf-8 -*-


from model.PhenotypeData import PhenotypeData

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from util.sql.Base import Base


## Class Individual
#  ================
#
# Each instance of object Individual is an individual issued from the data
# phenotypic file.
# An Individual object own :
#    - name: (String) describing his name.
#    - id: (Integer) giving his identifier in his Strain.
#    - date: (String) telling the date when the Individual was observed.
#    - age: (Integer) age (in week) for this Individual.
#    - sex: (String) 'm' (male) or 'f' (female)
#    - user: (String) the software user who input the phenotypic datas.
#    - data_list: list<PhenotypeData> related to this Individual.
#    - strain_number: (String) the Strain number for this Individual.
class Individual(Base):
    __tablename__ = 'individual'

    name = Column(String, primary_key=True)
    id = Column(Integer)
    date = Column(String)
    age = Column(Integer)
    sex = Column(String)
    user = Column(String)
    data_list = relationship('PhenotypeData', backref='individual_associated', cascade='all, delete-orphan')
    strain_number = Column(String, ForeignKey('strain.number'))
    # strain_associated = variable created by the backref in 'Strain'

    ## get_strain_number
    #  -----------------
    #
    # @return strain number.
    def get_strain_number(self):
        return self.strain_number


    # get_name
    # --------
    #
    # @return self.name.
    def get_name(self):
        return self.name

    # add_data
    # -------
    #
    # add PhenotypeData Individual object.
    #
    #    @param value : PhenotypeData object
    #
    # @return None
    def add_data(self, value):
        self.data_list.append(value)
        return

    # get_date
    # ----------
    #
    # @return self.date.
    def get_date(self):
        return self.date


    # get_strain
    # ----------
    #
    # @return the object Strain associated to this Individual
    def get_strain(self):
        return self.strain_associated

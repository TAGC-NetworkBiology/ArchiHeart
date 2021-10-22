# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, Integer, ForeignKey
from util.sql.Base import Base
from util import Constants
from util.log.Logger import Logger



## Class MutationEffect
#  ====================
#
# Each instance of this class is a MutationEffect object.
# Each MutationEffect object has:
#    - mutation_effect_id:(Integer) autoincremented identifier.
#    - flybase_id:(String) the flybase ID corresponding to the gene affected by this MutationEffect.
#    - symbol: (String) symbol gene related to the gene affected by this MutationEffect.
#    - position: (String) relative position to the gene.
#    - type: (String) effect's type.
#    - mutation_id: (String) responsible Mutation's mutation_id.
#    - mutation: (Mutation) the responsible Mutation.
class MutationEffect(Base):
    __tablename__ = 'mutation_effect'

#     mutation_effect_id = Column(Integer, primary_key=True, autoincrement=True)
    flybase_id = Column(String, primary_key=True)
    symbol = Column(String)
    mutation_id = Column(String, ForeignKey('mutation.mutation_id'), primary_key=True)
    position = Column(String)
    type = Column(String)
    
    # mutation = created by the many-to-one relationship in between Mutation
    #            and MutationEffect.

    # get_mutation
    # ------------
    #
    # Return mutation object associated to this mutation_effect.
    #
    # @return Mutation
    def get_mutation(self):
        return self.mutation

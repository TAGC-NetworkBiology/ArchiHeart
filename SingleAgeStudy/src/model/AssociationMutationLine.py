# -*- coding: utf-8 -*-

from sqlalchemy import Column, String

from util.sql.Base import Base
from sqlalchemy.sql.schema import ForeignKey, Index
from model.Line import Line


## Class AssociationMutationLine
#  =============================
#
# An AssociationMutationLine instance is an object containing a couple
# of mutation id and line id.
# This object is a link between Line and Mutation objects.
# An AssociationMutationLine object is inserted in database.
class AssociationMutationLine(Base):
    __tablename__ = 'mutation_in_line'

    mutation_id = Column(String, ForeignKey('mutation.mutation_id'),
                          primary_key=True)

    line_id = Column(String, ForeignKey('line.line_id'),
                      primary_key=True)


#     index_association = Index(mutation_id, line_id)




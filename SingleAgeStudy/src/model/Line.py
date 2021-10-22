# -*- coding: utf-8 -*-
from sqlalchemy import Column, String

from util.sql.Base import Base

## Class Line
#  ==========
#
# Each instance of this class is a line (strain) issued from DGRP genotype
# file. An object Line own a line_id lie 'dgrp340' and a list of mutations.
# This list of mutations is created by a many-to-many relationship between
# Mutation class and Line class.
class Line(Base):
    __tablename__ = 'line'

    line_id = Column(String, primary_key=True)
    # mutations = created by the many-to-many relationship between Mutation
    #            and Line.


    # get_line_id
    # -----------
    #
    # @return the line_id.
    def get_line_id(self):
        return self.line_id

    # get_mutations
    # -------------
    #
    # @return the list of object Mutation.
    def get_mutations(self):
        return self.mutations

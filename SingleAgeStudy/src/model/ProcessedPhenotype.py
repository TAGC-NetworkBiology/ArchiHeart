# -*- coding: utf-8 -*-


from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import PrimaryKeyConstraint

from util.sql.Base import Base
from model.ProcessedMutation import ProcessedMutation
from model.ProcessedPhenotypeData import ProcessedPhenotypeData
from model.ProcessedStrain import ProcessedStrain
from operator import attrgetter, methodcaller
from util.exception.ProcessedPhenotypeException import ProcessedPhenotypeException
from model.AnalyzedGene import AnalyzedGene
from model.AnalyzedPhenotype import AnalyzedPhenotype


# # Class ProcessedPhenotype
#  ======================
#
#  Each instance of this class is a studied phenotype.
# A studied phenotype has a name (exemple : 'Heartrate_Mean'), a method to study
# its data ( among : 'mean', 'IQR', '1.5IQR'), a list of processed data
# ( list of ProcessedPhenotypeData), a list of ProcessedStrain object, a list
# of ProcessedMutation objects.
#
# A ProcessedPhenotype is added to database SQL file with all its child (objects
# ProcessedPhenotypeData, ProcessedMutation, ProcessedStrain).
class ProcessedPhenotype( Base ):
    __tablename__ = 'processed_phenotype'

    # # @b Variables @b of @b ProcessedPhenotype:
    #
    #     - name: phenotype's name (e.g 'Heartperiod_Mean')
    #     - method: method to use to analyze phenotype with the data. (e.g 'IQR')
    #     - processed_data_list: list<ProcessedPhenotypeData>
    #     - processed_strain_list: list<ProcessedStrain>
    #     - processed_mutation_list: list<ProcessedMutation>
    name = Column( String )
    age = Column( Integer )
    method = Column( String )
    processed_data_list = relationship( 'ProcessedPhenotypeData', backref = 'processed_phenotype', cascade = 'all, delete-orphan' )
    processed_strain_list = relationship( 'ProcessedStrain', backref = 'processed_phenotype', cascade = 'all, delete-orphan' )
    processed_mutation_list = relationship( 'ProcessedMutation', backref = 'processed_phenotype', cascade = 'all, delete-orphan' )
    analyzed_phenotype_list = relationship( 'AnalyzedPhenotype', backref = 'processed_phenotype', cascade = 'all, delete-orphan' )

    __table_args__ = ( 
        PrimaryKeyConstraint( 'name', 'method', 'age' ),
    )

    # # add_gene
    #  --------
    #
    # Add Analyzedgene to ProcessedPhenotype
    #
    def add_gene( self, gene ):
        if isinstance( gene, AnalyzedGene ) == False:
            raise ProcessedPhenotypeException( '"gene" can not be added '
                                            'to ProcessedPhenotype object,'
                                            ' "gene" is not an instance of'
                                            'AnalyzedGene: '\
                                            , gene )
        self.analyzed_gene_list.append( gene )
        return

    # # sort_processed_strain
    #  ------------------
    #
    # Sort strains' reference values in order to class the strains.
    # Return sorted ProcessedStrain list.
    #
    # @return List<ProcessedStrain>
    def sort_processed_strain( self ):
        result = sorted( self.processed_strain_list, key = attrgetter( 'reference_value' ) )

        return result

    # # sort_polymorphism
    #  -----------------
    #
    # Sort polymorphism (ProcessedMutation objects)
    # in function of their Pi (weight).
    # Return result sorted processed mutation list.
    #
    # @return List<ProcessedMutation>
    def sort_processed_mutation( self ):
        
        result = sorted( self.processed_mutation_list, key = attrgetter( 'weight' ) )
        
        
        
        return result


    # # add_mutation
    #  ------------
    #
    # Add ProcessedMutation to processed_mutation_list.
    #
    # @param mutation: ProcessedMutation object to add to the ProcessedPhenotype
    #
    # @return None
    def add_mutation( self, processed_mutation ):
        try:
            processed_mutation
        except NameError:
            raise ProcessedPhenotypeException( '"processed_mutation" can not be'
                        ' added to ProcessedPhenotype object.' )
        # Test if mutation is a ProcessedMutation object.
        if isinstance( processed_mutation, ProcessedMutation ) == False:
            raise ProcessedPhenotypeException( '"processed_mutation" can not be'
                                    ' added to ProcessedPhenotype object, mutation'
                                    ' is not an instance of ProcessedMutation: '\
                                    , processed_mutation )

        self.processed_mutation_list.append( processed_mutation )

        return

    # # add_processed_data
    #  ------------------
    #
    # Add one ProcessedPhenotypeData object to processed_data_list.
    #
    # @param data: ProcessedPhenotypeData to add to the ProcessedPhenotype
    #
    # @return None
    def add_processed_data( self, processed_data ):
        try:
            processed_data
        except NameError:
            raise ProcessedPhenotypeException( '"processed_data" can not be added '
                                            'to ProcessedPhenotype object.' )

        # Test if data is a ProcessedPhenotypeData object.
        if isinstance( processed_data, ProcessedPhenotypeData ) == False:
            raise ProcessedPhenotypeException( '"processed_data" can not be added '
                                            'to ProcessedPhenotype object,'
                                            ' data is not an instance of'
                                            'ProcessedPhenotypeData: '\
                                            , processed_data )

        self.processed_data_list.append( processed_data )

        return

    # # add_processed_strain
    #  --------------------
    #
    # Add one ProcessedStrain object to processed_strain_list.
    #
    # @param processed_strain: ProcessedStrain object to add to the
    # ProcessedPhenotype
    #
    # @return None
    def add_processed_strain( self, processed_strain ):
        try:
            processed_strain
        except NameError:
            raise ProcessedPhenotypeException( 'Processed_strain can not be added'
                                            ' to '
                                            'ProcessedPhenotype object.' )
        # Test if processed_strain is a ProcessedStrain object.
        if isinstance( processed_strain, ProcessedStrain ) == False:
            raise ProcessedPhenotypeException( 'Processed_strain can not be added'
                                            ' to '
                                            'ProcessedPhenotype object,'
                                            ' processed_strain is not an'
                                            ' instance of'
                                            'ProcessedStrain: '\
                                            , processed_strain )

        self.processed_strain_list.append( processed_strain )

        return

    # # add_analyzed_phenotype
    #   ----------------------
    #
    # Add a relation to an AnalyzedPhenotype
    #
    # @param analyzed_phenotype : AnalyzedPhenotype - The AnalyzedPhenotype to make relation with
    #
    # @return None
    def add_analyzed_phenotype( self, analyzed_phenotype ):
        
        if analyzed_phenotype != None:
            self.analyzed_phenotype_list.append( analyzed_phenotype )

    # # get_name
    #  --------
    #
    # Return self.name
    #
    # @return String
    def get_name( self ):
        return self.name

    # # get_age
    #  -------
    #
    # Return self.age
    #
    # @return Integer
    def get_age( self ):
        return self.age

    # # get_mutation_list
    #  -----------------
    #
    # Return self.processed_mutation_list
    #
    # @return List<ProcessedMutation>
    def get_mutation_list( self ):
        return self.processed_mutation_list


    # # get_data_list
    #  -------------
    #
    # Return self.processed_data_list
    #
    # @return List<ProcessedPhenotypeData>
    def get_data_list( self ):
        return self.processed_data_list

    # # get_processed_strain_list
    #  -------------------------
    #
    # Return self.processed_data_list
    #
    # @return List<ProcessedStrain>
    def get_processed_strain_list( self ):
        return self.processed_strain_list


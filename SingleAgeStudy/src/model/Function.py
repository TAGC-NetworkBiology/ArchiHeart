# -*- coding: utf-8 -*-

from model.GO import GO

class Function(GO):
    
    def __init__(self, protein_symbol, protein_id, go_id, go_name, evidence,
                 protein_taxon_name):
        GO.__init__(self, protein_symbol, protein_id, go_id, go_name, evidence,
                 protein_taxon_name)
        

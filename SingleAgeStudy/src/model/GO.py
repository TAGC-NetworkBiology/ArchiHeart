# -*- coding: utf-8 -*-

class GO(object):

    def __init__(self, protein_symbol, protein_id, go_id, go_name, evidence,
                 protein_taxon_name):
        self.evidence = evidence
        self.goID = go_id
        self.goName = go_name
        self.proteinSymbol = protein_symbol
        self.proteinID = protein_id
        self.taxon = protein_taxon_name

    # get_evidence
    # ------------
    #
    # Return the evidence for this functional GO.
    def get_evidence(self):
        return self.evidence

    # get_go_ID
    # ---------
    #
    # Return the GO ID for this GO.
    def get_go_ID(self):
        return self.goID

    # get_go_name
    # -----------
    #
    # Return the GO name for this GO.
    def get_go_name(self):
        return self.goName

    # get_protein_symbol
    # ------------------
    #
    # Return the protein symbol for this GO.
    def get_protein_symbol(self):
        return self.proteinSymbol

    # get_protein_ID
    # --------------
    #
    # Return the protein ID for this GO.
    def get_protein_ID(self):
        return self.proteinID

    # get_taxon
    # ---------
    #
    # Return the taxon for this GO.
    def get_taxon(self):
        return self.taxon

    def __str__(self):
        string = self.evidence + '\t' + self.goID + '\t' + self.goName + '\t'\
        + self.proteinSymbol + '\t' + self.proteinID + '\t' + self.taxon
        return string

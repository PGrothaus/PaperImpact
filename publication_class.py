import numpy as np

class Publication:
    def __init__( self, recid=0, authors=[], affiliations=[],title='',\
                        abstract = '', nCitations = 0 ):
        
        self.authorList = authors
        self.nCitations = nCitations
        self.recid      = recid
        self.title      = title
        self.abstract   = abstract
        self.affiList   = affiliations

    def add_author( self, author ):
        self.authorList.append( str(author) )
    
    def add_affiliation( self, affiliation ):
        self.affiList.append( str(affiliation) )

    def set_title( self, title ):
        self.title = str(title)

    def set_abstract( self, abstract ):
        self.abstract = str(abstract)

    def set_recid( self, recid ):
        self.recid = recid

    def set_nCitations( self, nCitations ):
        self.nCitations = nCitations



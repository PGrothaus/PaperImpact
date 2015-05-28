import urllib
import json
import time
import publication_class
from publication_class import *

i=0
total=0
tot_time=0
for j in range( 1 ):
    t0=time.time()
    url='http://inspirehep.net/search?d1y=2000&d2y=2015&ot='\
        +'recid,authors,prepublication,title,abstract,number_of_citations,'\
        +'affiliation,citation&of=recjson&rg=250&jrec={0}'.format(total)

    data = json.loads(urllib.urlopen(url).read())

    pubList = []
    for datum in data:
        if datum['prepublication']:
            pub = Publication()
            #try:
            #print i, datum['recid'],\
            #         datum['prepublication']['date'],\
            #         datum['number_of_citations']
            pub.set_recid( int(datum['recid']) )
            pub.set_title( str(datum['title']['title']) )
            try:
                abstract = str(datum['abstract']['summary'])
                pub.set_abstract( abstract )
            #Abstract can be empty or contain weird characters
            except TypeError or UnicodeEncodeError:
                continue

            for author in datum['authors']:
                try:
                    lastName  = str(author['last_name'])
                    firstName = str(author['first_name'])
                    pub.add_author( lastName+','+firstName )
                #There can be weird characters in names
                except UnicodeEncodeError:
                    continue                    
                #print '\t{0}, {1}'.format(author['last_name'],\
                #                          author['first_name'])

            #Affiliation seems to be None
            try:
                for affiliation in datum['affiliation']:
                    pub.add_affiliation( str(affiliation) )
            except TypeError:
                pass

            pub.set_nCitations = int(datum['number_of_citations'])
            #if datum['number_of_citations']>0:
            #    print datum['citation']
            #except:
            #    continue
            pubList.append( pub )
            i += 1
        total += 1

    print pubList[3].title
    time_taken=time.time()-t0
    tot_time+=time_taken
    print 'Took {0} s'.format(time_taken), ' Total: {0} s'.format(tot_time)
    print   


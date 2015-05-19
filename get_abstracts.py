import urllib

#THIS IS A STUPID WAY OF DOING IT. SHOULD USE XML PARSER

f = open('test_corpus.txt', 'w')

url = 'http://export.arxiv.org/api/query?search_query=cat:hep-ph&start=0&max_results=2000'
data = urllib.urlopen(url).read()

words=data.split( )
abstract=False
abstr=[]
for word in words:
	if word=='<summary>':
		abstract=True
		continue
	if word=='</summary>':
		abstract=False
		abstr.append("\n")
		f.write(" ".join(abstr))
		abstr=[]
	if abstract==True:
		abstr.append(word)


url = 'http://export.arxiv.org/api/query?search_query=cat:hep-th&start=0&max_results=2000'
data = urllib.urlopen(url).read()

words=data.split( )
abstract=False
abstr=[]
for word in words:
	if word=='<summary>':
		abstract=True
		continue
	if word=='</summary>':
		abstract=False
		abstr.append("\n")
		f.write(" ".join(abstr))
		abstr=[]
	if abstract==True:
		abstr.append(word)


import random
with open('test_corpus.txt','r') as source:
    data = [ (random.random(), line) for line in source ]
data.sort()
with open('test_corpus_shuf.txt','w') as target:
    for _, line in data:
        target.write( line )		

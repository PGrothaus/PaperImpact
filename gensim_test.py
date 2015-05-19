import numpy as np
import cPickle as pickle
from gensim import corpora, models, similarities
import re, os, logging,sys

logging.basicConfig(format='%(message)s', level=logging.INFO)
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def line2list(line):
	return line.lower().replace('$','').replace('\\','').replace('-','').replace('.','').split()

def create_corpus(text_file,min_word_freq,save_dir, corpus_name, dict_name):
	path=os.getcwd()

	if save_dir not in os.listdir(path):
		os.mkdir(path+'/'+save_dir)

	class MyCorpus(object):
		def __iter__(self):
	         for line in open(text_file):
	            # assume there's one document per line, tokens separated by whitespace
	            yield dictionary.doc2bow(line2list(line))

	stoplist = set('we for a of the and to in is that shown show are than\
				 not such into some may its but would has only have will\
				 with at by an be this as from on which these it can between\
				 been all also find been or = there their if when no'.split())

	dictionary = corpora.Dictionary(line2list(line) for line in open(text_file))
	stop_ids = [dictionary.token2id[stopword] for stopword in stoplist
	             if stopword in dictionary.token2id]

	n=min_word_freq
	once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq < n]
	dictionary.filter_tokens(stop_ids + once_ids) # remove stop words and words that appear less that n times
	dictionary.compactify() # remove gaps in id sequence after words that were removed

	#save_dict
	with open(save_dir+'/'+dict_name+'.pkl', 'wb') as f:
		pickle.dump(dictionary,f)
	#create serializef corpus and save
	corpus = MyCorpus()
	corpora.MmCorpus.serialize(save_dir+'/'+corpus_name+'.mm', corpus)

def main(query,lda_params,load_dir='tmp',lda_model_file='hep-ph_th.lda',corpus_text_file='test_corpus_shuf.txt', min_word_freq=5,corpus_name='corpus', dict_name='dict'):
	try: 
		corpus = corpora.MmCorpus(load_dir+'/'+corpus_name+'.mm')
		with open(load_dir+'/'+dict_name+'.pkl', 'rb') as f:
			dictionary=pickle.load(f)
	except:
		print bcolors.WARNING + "Could not find precomputed corpus. Creating now..." + bcolors.ENDC
		create_corpus(text_file=corpus_text_file,min_word_freq=min_word_freq,save_dir=load_dir, corpus_name=corpus_name, dict_name=dict_name)
		corpus = corpora.MmCorpus(load_dir+'/'+corpus_name+'.mm')
		with open(load_dir+'/'+dict_name+'.pkl', 'rb') as f:
			dictionary=pickle.load(f)

	print (bcolors.OKGREEN+'CORPUS: {0}' + bcolors.ENDC).format(corpus)
	try:
		lda = models.LdaModel.load(load_dir+'/'+lda_model_file)
	except:
		print bcolors.WARNING + 'No LDA model found. Training LDA now' + bcolors.ENDC
		lda = models.ldamodel.LdaModel(corpus=corpus,  id2word=dictionary,
				 			alpha=lda_params['alpha'],num_topics=lda_params['num_topics'],\
				 			update_every=lda_params['update_every'], chunksize=lda_params['chunksize'],\
				 			passes=lda_params['passes'])

		lda.save(load_dir+'/'+lda_model_file)
		lda = models.LdaModel.load(load_dir+'/'+lda_model_file)


	print bcolors.OKBLUE+'MODEL PREVIEW:'
	topics=lda.show_topics(num_topics=5, num_words=5)
	for topic in topics:
		print topic
	print bcolors.ENDC


	query = dictionary.doc2bow(line2list(query))
	a = list(sorted(lda[query], key=lambda x: x[1],reverse=True) )

	print bcolors.OKGREEN+'QUERY OUTPUT:'
	for i in range(len(a)):
		print a[i][1],lda.print_topic(a[i][0])
	print bcolors.ENDC

if __name__ == '__main__':
	
	query='We consider the effect of a period of inflation with a high energy density upon the stability of the Higgs potential in the early universe. The recent measurement of a large tensor-to-scalar ratio, $r_T \sim 0.16$, by the BICEP-2 experiment possibly implies that the energy density during inflation was very high, comparable with the GUT scale. Given that the standard model Higgs potential is known to develop an instability at $\Lambda \sim 10^{10}$ GeV this means that the resulting large quantum fluctuations of the Higgs field could destabilize the vacuum during inflation, even if the Higgs field starts at zero expectation value. We estimate the probability of such a catastrophic destabilisation given such an inflationary scenario and calculate that for a Higgs mass of $m_h=125.5$ GeV that the top mass must be less than $m_t\sim 172$ GeV. We present two possible cures: a direct coupling between the Higgs and the inflaton and a non-zero temperature from dissipation during inflation.'
	LDA_PARAMS={
	'alpha':'auto',
	'num_topics': 5,
	'update_every': 1,
	'chunksize': 1000,
	'passes': 500 
	}
	main(query,LDA_PARAMS)	


'''
Created on 04.08.2017

@author: christian
'''

import nltk
from nltk.corpus import EuroparlCorpusReader
from nltk.metrics import BigramAssocMeasures
from nltk.collocations import BigramCollocationFinder
from nltk.corpus import stopwords as stop_corpus
import treetaggerwrapper

def content_fraction(text):
    stopwords = stop_corpus.words('german')
    content = [w for w in text if w.lower() not in stopwords]
    return len(content)*1. / len(text)

def lexical_diversity(my_text_data):
    word_count = len(my_text_data)*1.
    vocab_size = len(set(my_text_data))
    diversity_score = vocab_size / word_count
    return diversity_score

def unusual_words(text, nltk_data_dir="/usr/share/nltk_data/"):
    text_vocab = set(text)
    
    reader = EuroparlCorpusReader(nltk_data_dir + "corpora/europarl_raw/german",
                                  ["ep-00-01-17.de","ep-00-01-18.de","ep-00-01-19.de","ep-00-01-20.de",
                                   "ep-00-01-21.de","ep-00-02-02.de","ep-00-02-03.de","ep-00-02-14.de",
                                   "ep-00-02-15.de", "ep-00-02-16.de"])
    german_vocab = set(w.lower() for w in reader.words())
    unusual = text_vocab - german_vocab
    return sorted(unusual)

def collocations(nltk_txt, num=20, window_size=2):
    """
    Print collocations derived from the text, ignoring stopwords.

    :seealso: find_collocations
    :param num: The maximum number of collocations to print.
    :type num: int
    :param window_size: The number of tokens spanned by a collocation (default=2)
    :type window_size: int
    """
    if not ('_collocations' in nltk_txt.__dict__ and nltk_txt._num == num and nltk_txt._window_size == window_size):
        nltk_txt._num = num
        nltk_txt._window_size = window_size

        #print("Building collocations list")
        ignored_words = stop_corpus.words('german')
        finder = BigramCollocationFinder.from_words(nltk_txt.tokens, window_size)
        finder.apply_freq_filter(2)
        finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in ignored_words)
        bigram_measures = BigramAssocMeasures()
    
        nltk_txt._collocations = [(p[0] + " " + p[1], s)
                                  for p, s in finder.score_ngrams(bigram_measures.likelihood_ratio)[:num]]
        
    colloc_strings = dict(nltk_txt._collocations)
    return colloc_strings

import os

def analyze_keytextmarkers(doc_info, fname):
    print "Analyze text markers"
    
    txt_name = fname[:-3] + "txt"
    tok_name = fname[:-3] + "tok"
    csv_name = fname[:-3] + "csv"
    os.system("pwd")
    os.system("ucto -L de -n -s \".\" %s %s" % (txt_name, tok_name))
    os.system("readability --csv %s > %s" % (tok_name, csv_name))
    
    f = open(csv_name)
    line1 = f.readline().split(",")
    line2 = f.readline().split(",")
    f.close()
    
    for item_name, item_val in zip(line1, line2):
        if item_name != "":
            doc_info[item_name] = item_val

def analyze_tags(doc_info, ts):
    print "Analyze tagging"
    
    strip_tags = [t for t in ts if isinstance(t, treetaggerwrapper.Tag)]
    pron = [t.lemma for t in strip_tags if t.pos.startswith("PP")]
    
    stopwords = stop_corpus.words('german')
    strip_tags = [t for t in strip_tags if t.lemma.lower() not in stopwords]
    
    nouns = [t.lemma for t in strip_tags if t.pos == "NN"]
    verbs = [t.lemma for t in strip_tags if t.pos[0] == "V"]
    adj = [t.lemma for t in strip_tags if t.pos == "ADJA"]
    
    lemmas = map(lambda x: x.lemma, strip_tags)
    positions = map(lambda x: x.pos, strip_tags)
    
    doc_info["tag_words"] = len(ts)
    doc_info["tag_words_identified"] = len(strip_tags)
    doc_info["tag_lemmas"] = len(set(lemmas))
    doc_info["tag_pos"] = len(set(positions))
    
    fdist_lemma = nltk.FreqDist(lemmas)
    fdist_pos = nltk.FreqDist(positions)
    
    doc_info["tag_lemma20"] = dict([(tup[0], tup[1]*1./doc_info["tag_words_identified"]) for tup in fdist_lemma.most_common(20)])
    
    
    doc_info["tag_pos"] = [{"pos": tup[0],
                            "frequency": tup[1]*1./doc_info["tag_words_identified"]} for tup in fdist_pos.most_common(100)]
    
    for word_list, wname in zip([nouns, adj, verbs, pron], ["nouns20", "adj20", "verb20", "pron10"]):
        fdist = nltk.FreqDist(word_list)
        doc_info[wname] = dict([(tup[0], tup[1]) for tup in fdist.most_common(20)])

def analyze_page_text(doc_info, page_text):
    print "Analyze NLTK"
    
    fdist1 = nltk.FreqDist(page_text)
    #fdist1.plot(50, cumulative=True)
    doc_info["important_words_7"] = dict([(w, fdist1[w])
                                     for w in set(page_text) if len(w) > 7 and fdist1[w] > 7])
    
    doc_info["collocations_30"] = collocations(page_text, 30)
    doc_info["lexical_diversity"] = lexical_diversity(page_text)
    doc_info["content_fraction"] = content_fraction(page_text)
    #print unusual_words(page_text)
    
# -*- coding: latin-1 -*-
'''
Created on 27.07.2017

@author: christian
'''

import nltk
import slate
import treetaggerwrapper
import readability

from nltk.corpus import EuroparlCorpusReader



def lexical_diversity(my_text_data):
    word_count = len(my_text_data)*1.
    vocab_size = len(set(my_text_data))
    diversity_score = vocab_size / word_count
    return diversity_score

def unusual_words(text):
    text_vocab = set(text)
    
    reader = EuroparlCorpusReader("/home/christian/nltk_data/corpora/europarl_raw/german",
                                  ["ep-00-01-17.de","ep-00-01-18.de","ep-00-01-19.de","ep-00-01-20.de",
                                   "ep-00-01-21.de","ep-00-02-02.de","ep-00-02-03.de","ep-00-02-14.de",
                                   "ep-00-02-15.de", "ep-00-02-16.de"])
    german_vocab = set(w.lower() for w in reader.words())
    unusual = text_vocab - german_vocab
    return sorted(unusual)

def content_fraction(text):
    stopwords = nltk.corpus.stopwords.words('german')
    content = [w for w in text if w.lower() not in stopwords]
    return len(content)*1. / len(text)

def analyze_tags(doc_info, ts):
    strip_tags = [t for t in ts if isinstance(t, treetaggerwrapper.Tag)]
    lemmas = map(lambda x: x.lemma, strip_tags)
    positions = map(lambda x: x.pos, strip_tags)
    
    doc_info["tag_words"] = len(ts)
    doc_info["tag_words_identified"] = len(strip_tags)
    doc_info["tag_lemmas"] = len(set(lemmas))
    doc_info["tag_pos"] = len(set(positions))
    
    fdist_lemma = nltk.FreqDist(lemmas)
    fdist_pos = nltk.FreqDist(positions)
    
    doc_info["tag_lemma20"] = [{"lemma": tup[0],
                                "frequency": tup[1]*1./doc_info["tag_words_identified"]} for tup in fdist_lemma.most_common(20)]
    
    
    doc_info["tag_pos"] = [{"pos": tup[0],
                            "frequency": tup[1]*1./doc_info["tag_words_identified"]} for tup in fdist_pos.most_common(100)]

def analyze_page_text(doc_info, page_text):
    fdist1 = nltk.FreqDist(page_text)
    #fdist1.plot(50, cumulative=True)
    doc_info["important_words_7"] = [{"word": w, "frequency": fdist1[w]}
                                     for w in set(page_text) if len(w) > 7 and fdist1[w] > 7]
    
    doc_info["collocations_30"] = page_text.collocations(30)
    
    doc_info["lexical_diversity"] = lexical_diversity(page_text)
    doc_info["content_fraction"] = content_fraction(page_text)
    #print unusual_words(page_text)

import os

def analyze_keytextmarkers(doc_info, fname):
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

def get_infos(keys, info):
    res = []
    for key in keys:
        try:
            if key.startswith("pos"):
                res.append(str(info["tag_pos"][key[3:]]))
            else:
                res.append(str(info[key]))
        except:
            res.append(str(0.))
    return res

def analyze_document(party, year):
    doc_info = {}
    doc_info["party"] = party
    doc_info["year"] = year

    base_dir = "/home/christian/Programming/data/Wahlomat/Proper/"
    fname = base_dir + party + "/buwa_%s_%i.txt" % (party.lower(), year)
    print "Reading document: ", fname
    
    if not os.path.exists(fname):
        return None
    
    print "Analyze text markers"
    analyze_keytextmarkers(doc_info, fname)
    
    f = open(fname)
    #doc = "\n\n".join(slate.PDF(f)).lower()
    doc = "".join(f.readlines())
    f.close()
    
    #print doc
    #return None
    
    """
    paras = doc.split("\n\n")
    
    fname_new = fname[:-3] + "txt"
    f = open(fname_new, "w")
    for para in paras:
        print >>f, para.replace("(cid:173)\n","").replace("\n", " "), "\n\n"
    f.close()
    return None
    """

    
    print "Analyze tagging"
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='de', TAGDIR="/home/christian/nltk_data/tree_tagger")
    tags = tagger.tag_text(doc.decode("utf-8"))
    tags2 = treetaggerwrapper.make_tags(tags)
    analyze_tags(doc_info, tags2)
    
    print "Analyze NLTK"
    page_text = nltk.Text(nltk.word_tokenize(doc.decode("latin-1"), 'german', False))
    analyze_page_text(doc_info, page_text)
    return doc_info

if __name__ == "__main__":
    from pymongo import MongoClient
    mongo_connector = MongoClient("mongodb://localhost:27017")
    polit_data = mongo_connector["policy_analysis"].wahlprogramme
    res_dir = "/home/christian/Programming/data/Wahlomat/Proper/"
    
    baseinfo_keys = ['year', 'party', 'characters', 'words', 'paragraphs', 'syllables', 'sentences'
                'tag_lemmas', 'tag_words','tag_words_identified' ,'long_words', "complex_words"]
    
    basestat_keys = ['year', 'party','syll_per_word', 'words_per_sentence', 'characters_per_word',
                     'content_fraction', 'lexical_diversity', 'wordtypes\n', 'sentences_per_paragraph']
    
    readability_keys = ['year', 'party', 'DaleChallIndex', 'LIX', 'Coleman-Liau', 'RIX',
                        'GunningFogIndex', 'SMOGIndex','FleschReadingEase','Kincaid',
                        'ARI']
    
    pos_stat_keys = ['year', 'party', 'posNN', 'posART', 'posADJA', 'posAPPR','posKON',
                     'posVVFIN', 'posADV', 'posVAFIN', 'posVVINF', 'posADJD', 
                     'posVVPP', 'posNE', 'posVMFIN', 'posAPPRART', 'posPPER',
                     'posKOUS', 'posPIAT', 'posVAINF', 'posPTKZU', 'posPAV',
                     'posPPOSAT', 'posPRELS', 'posFM', 'posTRUNC', 'posPTKNEG',
                     'posCARD', 'posVVIZU', 'posPRF', 'posPTKVZ', 'posPDAT',
                     'posPIS', 'posKOKOM', 'posPDS', 'posKOUI', 'posPWAV',
                     'posVMINF', 'posPRELAT', 'posPWS', 'posXY', 'posPTKA',
                     'posVAPP', 'posVVIMP', 'posAPZR'] 
        
    word_cloud_keys = ['important_words_7']
    restypes = [baseinfo_keys, basestat_keys, readability_keys, pos_stat_keys]
    resf = []
    for res_keys, resname in zip(restypes,
                                 ["baseinfo", "basestat", "readability", "posinfo"]):
        resf.append(open(res_dir + "results_%s.csv" % resname, "w"))
        print >> resf[-1], ",".join(res_keys)
        
    res_keys = None
    for cur_party in ["CDU", "SPD", "FDP", "Green", "Linke","AFD"]:
        for cur_year in [1949, 1953, 1957, 1961, 1965, 1969,
                     1972, 1976, 1980, 1983, 1987, 1990,
                     1994, 1998, 2002, 2005, 2009, 2013,
                     2017]:
            doc_infos = analyze_document(cur_party, cur_year)
            if doc_infos != None:
                #polit_data.insert_one(doc_infos)
                for rnum, res_keys in enumerate(restypes):
                    print >> resf[rnum], ",".join(get_infos(res_keys, doc_infos))
    for f in resf:
        f.close()
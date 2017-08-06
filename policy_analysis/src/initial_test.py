# -*- coding: latin-1 -*-
'''
Created on 27.07.2017

@author: christian
'''

import nltk
import analyses
import preparations
import os
import result_writers


def analyze_document(base_dir, party, year):
    doc_info = {}
    doc_info["party"] = party
    doc_info["year"] = year

    fname = base_dir + party + "/buwa_%s_%i.txt" % (party.lower(), year)
    
    if not os.path.exists(fname):
        return None
    
    doc = preparations.read_txt_doc(fname)
    page_text = nltk.Text(nltk.word_tokenize(doc.decode("latin-1"), 'german', False))

    analyses.analyze_keytextmarkers(doc_info, fname)
    analyses.analyze_tags(doc_info, preparations.get_tags(doc))
    analyses.analyze_page_text(doc_info, page_text)
    
    return doc_info

def analyze_all_docs(data_dir, test=False):
    all_doc_infos = []
    for cur_party in ["CDU", "SPD", "FDP", "Green", "Linke","AFD"]:
        for cur_year in [1949, 1953, 1957, 1961, 1965, 1969,
                     1972, 1976, 1980, 1983, 1987, 1990,
                     1994, 1998, 2002, 2005, 2009, 2013,
                     2017]:
            doc_info = analyze_document(data_dir, cur_party, cur_year)
            
            if doc_info != None:
                all_doc_infos.append(doc_info)
            if test:
                break
        if test:
            break
    return all_doc_infos

if __name__ == "__main__":
    info_dir = "../data/Cleaned/"
    res_dir = "../docs/results/"
    
    doc_infos = analyze_all_docs(info_dir, False)
    result_writers.write_results_to_csv(doc_infos, res_dir)
    
'''
Created on 04.08.2017

@author: christian
'''

import treetaggerwrapper

def read_txt_doc(fname):
    print "Reading document: ", fname
    f = open(fname)
    doc = "".join(f.readlines())
    f.close()
    
    return doc
    
def get_tags(doc):
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='de', TAGDIR="/opt/tree_tagger")
    tags = tagger.tag_text(doc.decode("utf-8"))
    return treetaggerwrapper.make_tags(tags)
    
def correct_paragraphs():
    
        
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

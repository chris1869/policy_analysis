'''
Created on 04.08.2017

@author: christian
'''

from pymongo import MongoClient
from wordcloud import WordCloud

class TextKeyWriter():
    def __init__(self, tkeys, fname):
        self.target_keys =  tkeys
        self.fname = fname
        self._init_file()
    
    def _init_file(self):
        self._resf = open(self.fname, "w")
        print >> self._resf, ",".join(self.target_keys)
    
    @staticmethod
    def _read_key(info, key):
        return str(info[key])
    
    def _read_info(self, info):
        res = []
        for key in self.target_keys:
            try:
                res.append(self._read_key(info, key))
            except:
                res.append(str(0.))
        return res
    
    def add_info(self, info):
        print >> self._resf, ",".join(self._read_info(info))
        
    def finalize(self):
        self._resf.close()
        

class FreqKeyWriter(TextKeyWriter):
    @staticmethod
    def _read_key(info, key):
        return str(info["tag_pos"][key[3:]])

class WordCloudWriter():
    def __init__(self, tkeys, res_dir):
        self.target_keys =  tkeys
        self.res_dir = res_dir
        self.wc = WordCloud()
        
    @staticmethod
    def _read_key(info, key):
        return info[key]
    
    def add_info(self, info):
        for key in self.target_keys:
            res_fname = self.res_dir + "/%s/buwa_%s_%s.png" % (key, info["party"], info["year"])
            self.wc.fit_words(self._read_key(info, key))
            self.wc.to_file(res_fname)

def gen_base_writers(res_dir):
    writers = []
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
        
    word_cloud_keys = ['important_words_7', "tag_lemma20", "collocations_30",
                       "nouns20", "adj20", "verb20", "pron10"]
    
    
    restypes = [baseinfo_keys, basestat_keys, readability_keys, pos_stat_keys, word_cloud_keys]
    
    for res_keys, resname in zip(restypes,
                                 ["baseinfo", "basestat", "readability", "posinfo", "word_clouds"]):
        if resname == "posinfo":
            writers.append(FreqKeyWriter(res_keys, res_dir + "results_%s.csv" % resname))
        elif resname == "word_clouds":
            writers.append(WordCloudWriter(res_keys, res_dir))
        else:
            writers.append(TextKeyWriter(res_keys, res_dir + "results_%s.csv" % resname))
    return writers

def write_results_to_mongodb(doc_infos, mongo_url="mongodb://localhost:27017"):    
    mongo_connector = MongoClient(mongo_url)
    polit_data = mongo_connector["policy_analysis"].wahlprogramme
    polit_data.insert_many(doc_infos)

def write_results_to_csv(doc_infos, res_dir):
    writers = gen_base_writers(res_dir)
    
    for writer in writers:
        for doc_info in doc_infos:
            try:
                writer.add_info(doc_info)
            except:
                pass
        try:
            writer.finalize()
        except:
            pass
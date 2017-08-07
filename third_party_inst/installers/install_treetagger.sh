mkdir /opt/tree_tagger

cd /opt/tree_tagger
wget http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tree-tagger-linux-3.2.1.tar.gz
wget http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/tagger-scripts.tar.gz
wget http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/install-tagger.sh
wget http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/german-par-linux-3.2-utf8.bin.gz
wget http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/data/german-chunker-par-linux-3.2-utf8.bin.gz

chmod 755 install-tagger.sh
./install-tagger.sh

wget https://github.com/LanguageMachines/uctodata/releases/download/v0.4/uctodata-0.4.tar.gz

tar xvzf uctodata-0.4.tar.gz

cd uctodata-0.4
chmod 755 bootstrap.sh
./bootstrap.sh
./configure
make
make install

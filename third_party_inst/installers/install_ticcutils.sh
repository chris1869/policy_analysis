
wget https://github.com/LanguageMachines/ticcutils/releases/download/v0.15/ticcutils-0.15.tar.gz
tar xvzf ticcutils-0.15.tar.gz

cd ticcutils-0.15
chmod 755 bootstrap.sh
./bootstrap.sh
./configure
make
make install

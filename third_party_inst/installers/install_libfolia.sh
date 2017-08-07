wget https://github.com/LanguageMachines/libfolia/releases/download/v1.7/libfolia-1.7.tar.gz
tar xvzf libfolia-1.7.tar.gz

cd libfolia-1.7
chmod 755 bootstrap.sh

./bootstrap.sh
./configure
make
make install

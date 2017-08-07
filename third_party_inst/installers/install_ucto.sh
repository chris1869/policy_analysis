wget https://github.com/LanguageMachines/ucto/releases/download/v0.9.6/ucto-0.9.6.tar.gz
tar -xvzf ucto-0.9.6.tar.gz

cd ucto-0.9.6
chmod 755 bootstrap.sh

bootstrap.sh
./configure
make
make install

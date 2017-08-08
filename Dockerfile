FROM nginx:stable-alpine

RUN apk add --update \
    automake \
    autoconf \
    python \
    python-dev \
    py-pip \
    build-base \
    git \
    nodejs \
    ca-certificates \
    openssl \
    libxml2-dev \
    musl-dev\
    icu-dev\
    file \
    libtool \
    freetype-dev \
    libpng-dev \
    jpeg-dev \
    libgomp

RUN update-ca-certificates
RUN pip install pymongo numpy matplotlib pandas nltk readability treetaggerwrapper wordcloud
RUN npm install -g http-server

RUN mkdir /opt
RUN mkdir /opt/policy_analysis/
ADD . /opt/policy_analysis/

WORKDIR /opt/policy_analysis/third_party_inst/installers

RUN patch -p0 < glob.patch
RUN chmod 755 install*.sh

RUN ./install_treetagger.sh
RUN ./install_ticcutils.sh
RUN ./install_libfolia.sh
RUN ./install_uctodata.sh
RUN ./install_ucto.sh

RUN apk del build-base python-dev automake autoconf libxml2-dev freetype-dev libpng-dev jpeg-dev musl-dev libtool

RUN cp -R ../nltk_data/ /usr/share/nltk_data/

ADD run_test.sh /opt/run_test.sh
RUN chmod 755 /opt/run_test.sh

EXPOSE 8080

CMD /opt/run_test.sh
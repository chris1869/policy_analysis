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
RUN pip install pymongo nltk readability treetaggerwrapper pandas wordcloud
RUN npm install -g http-server

RUN apk del build-base python-dev

RUN mkdir /opt
WORKDIR /opt/

RUN git clone https://chris1869:6a48048a9a94dffeebb0fcbacf85a7952190617d@github.com/chris1869/policy_analysis.git

WORKDIR /opt/policy_analysis/third_party_inst/installers

RUN chmod 755 install*.sh

RUN ./install_treetagger.sh

RUN patch -p0 < glob.patch
RUN ./install_ticcutils.sh
RUN ./install_libfolia.sh
RUN ./install_uctodata.sh
RUN ./install_ucto.sh

RUN cp -R ../nltk_data/ /usr/share/nltk_data/

ADD run_test.sh /opt/run_test.sh
RUN chmod 755 /opt/run_test.sh

EXPOSE 8080

CMD /opt/run_test.sh
FROM docker.io/library/postgres:alpine

RUN \ 
apk add -q --no-cache \
postgresql-contrib \
make \
git \
&& rm -rf /tmp/* /var/cache/apk/*

RUN git clone https://github.com/michelp/pgjwt.git
WORKDIR /pgjwt
RUN make install
WORKDIR /

RUN apk del git

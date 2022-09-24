FROM ubuntu:latest
#FROM resin/rpi-raspbian:jessie

RUN apt-get update
RUN apt-get install -y wget python3 python3-pip geoip-database python3-twisted \
      python3-libtorrent libsdl2-dev python3-pygame librsvg2-common xdg-utils \
      intltool
RUN python3 -m pip install -U pip
RUN pip3 install \
      setuptools \
      xdg \
      chardet \
      mako \
      requests \
      deluge
#    python-notify ?
#    glade2 ?

RUN apt-get clean
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    ln -s /usr/bin/python3 /usr/bin/python
WORKDIR /
RUN wget http://download.deluge-torrent.org/source/2.1/deluge-2.1.0.tar.xz && \
    tar -xf deluge-2.1.0.tar.xz && \
    rm deluge-2.1.0.tar.xz && \
    cd deluge-2.1.0 && \
    python setup.py build && \
    python setup.py install
RUN adduser --system -u 1000 deluge
EXPOSE 58846 8112
ADD start.sh /start.sh
COPY watch.py /watch.py
ENTRYPOINT ["/start.sh"]


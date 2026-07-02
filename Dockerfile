FROM neosmemo/memos:0.25.1

RUN apk update && apk add --no-cache \
    nginx \
    curl \
    wget \
    build-base \
    openssl-dev \
    zlib-dev \
    bzip2-dev \
    readline-dev \
    sqlite-dev \
    ncurses-dev \
    tk-dev \
    libffi-dev \
    xz-dev

RUN wget https://www.python.org/ftp/python/3.14.0/Python-3.14.0.tgz && \
    tar -xzf Python-3.14.0.tgz && \
    cd Python-3.14.0 && \
    ./configure --enable-optimizations --prefix=/usr/local && \
    make -j$(nproc) && \
    make install && \
    cd .. && \
    rm -rf Python-3.14.0 Python-3.14.0.tgz

RUN ln -sf /usr/local/bin/python3.14 /usr/local/bin/python && \
    ln -sf /usr/local/bin/pip3.14 /usr/local/bin/pip

COPY ./src/ /app/src
COPY ./nginx/yps.conf /etc/nginx/http.d/default.conf
COPY ./start.sh /start.sh

RUN pip install -r /app/src/requirements.txt

RUN chmod +x /start.sh

EXPOSE 80 3000 5240

CMD ["/start.sh"]
FROM neosmemo/memos:0.25.1

RUN apt-get update && apt-get install -y \
    nginx \
    curl \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    python3-openssl

RUN wget https://www.python.org/ftp/python/3.14.0/Python-3.14.0.tgz && \
    tar -xzf Python-3.14.0.tgz && \
    cd Python-3.14.0 && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make install && \
    cd .. && \
    rm -rf Python-3.14.0 Python-3.14.0.tgz

RUN ln -sf /usr/local/bin/python3.14 /usr/local/bin/python && \
    ln -sf /usr/local/bin/pip3.14 /usr/local/bin/pip

COPY ./src/ /app/src
COPY ./nginx/yps.conf /etc/nginx/sites-available/default
COPY ./start.sh /start.sh

RUN pip install -r /app/src/requirements.txt

RUN chmod +x /start.sh

EXPOSE 80

CMD ["/start.sh"]
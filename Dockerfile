

FROM neosmemo/memos:0.25.1

RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories && \
    apk update && \
    apk add --no-cache \
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
    iproute2 \
    findutils \
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
COPY ./entry.sh /entry.sh
RUN pip install -r /app/src/requirements.txt

RUN chmod +x /entry.sh

EXPOSE 80 3000 5230


# 赋予执行权限
RUN chmod +x /usr/local/memos/memos /entry.sh

# 核心：ENTRYPOINT 执行脚本，CMD置空
ENTRYPOINT ["/entry.sh"]
CMD []
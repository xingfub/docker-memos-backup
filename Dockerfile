FROM neosmemo/memos:0.25.1

RUN apk update && apk add --no-cache \
    nginx \
    curl \
    python3.14 \
    py3-pip \
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

RUN ln -sf /usr/bin/python3.14 /usr/bin/python && \
    ln -sf /usr/bin/pip3 /usr/bin/pip

COPY ./src/ /app/src
COPY ./nginx/yps.conf /etc/nginx/http.d/default.conf
COPY ./start.sh /start.sh

RUN pip install -r /app/src/requirements.txt

RUN chmod +x /start.sh

EXPOSE 80

CMD ["/start.sh"]
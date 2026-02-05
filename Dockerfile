FROM nginx:1.25.5-alpine

RUN apk add --no-cache \
    git gcc g++ make brotli-dev pcre2-dev zlib-dev openssl-dev \
    linux-headers wget ca-certificates

WORKDIR /usr/src

# Clone Brotli module
RUN git clone https://github.com/google/ngx_brotli.git \
    && cd ngx_brotli \
    && git submodule update --init --recursive

# Download nginx source
RUN wget http://nginx.org/download/nginx-1.25.5.tar.gz \
    && tar -xzf nginx-1.25.5.tar.gz

WORKDIR /usr/src/nginx-1.25.5

RUN ./configure \
    --with-compat \
    --add-dynamic-module=/usr/src/ngx_brotli \
    && make modules

RUN cp objs/ngx_http_brotli_filter_module.so /etc/nginx/modules/ \
    && cp objs/ngx_http_brotli_static_module.so /etc/nginx/modules/

RUN apk del git gcc g++ make wget linux-headers pcre2-dev zlib-dev openssl-dev brotli-dev \
    && rm -rf /usr/src

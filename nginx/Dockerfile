FROM nginx

RUN apt-get update && apt-get -y install openssl
RUN openssl req -x509 -newkey rsa:4096 -days 365 -nodes \
    -keyout /etc/ssl/private/test.kr_key.pem \
    -out /etc/ssl/certs/test.kr_cert.pem -sha256 \
    -subj "/C=KR/ST=Seoul/L=Seoul/O=42 Seoul/CN=test.kr"


COPY nginx.conf /usr/local/etc/nginx/nginx.conf

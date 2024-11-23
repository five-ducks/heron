FROM nginx

ARG SSL_PUBLIC_KEY \
	SSL_PRIVATE_KEY

RUN apt-get -y update && \
	apt-get -y upgrade && \
	apt-get -y install openssl dumb-init

RUN echo "$SSL_PUBLIC_KEY" > /etc/ssl/certs/localhost.dev.crt && \
	echo "$SSL_PRIVATE_KEY" > /etc/ssl/private/localhost.dev.key && \
	chmod 600 /etc/ssl/certs/localhost.dev.crt /etc/ssl/private/localhost.dev.key

COPY nginx.conf /etc/nginx/nginx.conf

WORKDIR /usr/share/nginx/html

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
ENTRYPOINT [ "dumb-init" ]
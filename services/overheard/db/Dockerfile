FROM tarantool/tarantool:1.10.2
RUN apk update && apk add gcc musl-dev git
WORKDIR /opt/tarantool
RUN apk add msgpuck-dev --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ --allow-untrusted
RUN cp /usr/lib/libmsgpuck.a libmsgpuck.a
COPY app.lua .
COPY keygen.so .
CMD ["tarantool", "app.lua"]
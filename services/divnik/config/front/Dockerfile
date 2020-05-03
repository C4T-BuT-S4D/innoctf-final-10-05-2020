FROM ubuntu:18.04

ENV PATH="/usr/local/flutter/bin:${PATH}"

RUN apt-get update && \
    apt-get install -y \
        unzip \
        xz-utils \
        git \
        openssh-client \
        curl && \
    rm -rf /var/cache/apt

RUN curl -L https://storage.googleapis.com/flutter_infra/releases/stable/linux/flutter_linux_v1.12.13+hotfix.9-stable.tar.xz | tar -C /usr/local/ -xJ

COPY ./front/ /app

ADD ./config/front/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
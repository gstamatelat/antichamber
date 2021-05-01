FROM alpine

RUN apk update
RUN apk upgrade

RUN apk add python3
RUN apk add potrace
RUN apk add imagemagick
RUN apk add texlive-full
RUN apk add poppler-utils

COPY . /root/antichamber/

ENTRYPOINT cd /root/antichamber/ && ash

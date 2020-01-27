FROM alpine:3.11
# Use alpine linux as base image

COPY . /home/web/

RUN apk add python3
RUN adduser --disabled-password web && mkdir -p /home/web/log/ && chown -R web.web /home/web/

USER web
WORKDIR /home/web


ENV PATH=$PATH:/home/web/.local/bin \
    SERVER=server

ENTRYPOINT [ "python3" ]
CMD ["client.py"]
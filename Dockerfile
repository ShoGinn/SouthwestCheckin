FROM python:3.7-alpine
COPY . /app/swcheckin/
RUN apk add --no-cache tini git && \
    pip install --no-cache-dir /app/swcheckin

ENTRYPOINT ["/sbin/tini", "--", "/app/swcheckin/docker-entrypoint.sh"]

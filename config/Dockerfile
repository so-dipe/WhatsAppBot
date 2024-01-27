FROM redis:7.0.1-alpine

WORKDIR /server

COPY redis.conf .

EXPOSE 6379

CMD ["redis-server", "redis.conf"]
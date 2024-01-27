
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN ./install.sh

EXPOSE 8000

CMD ["bash", "./run.sh"]

FROM python:3.10-slim

WORKDIR /app

# Install curl
RUN apt-get update && apt-get install -y curl

COPY . .

# RUN pip install -r requirements.txt
RUN ./install.sh

EXPOSE 8000

# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["bash", "./run.sh"]

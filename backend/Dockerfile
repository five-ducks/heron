FROM python:3

ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y dumb-init
RUN pip install -r requirements.txt && rm -f requirements.txt

ENTRYPOINT ["sh", "docker-entrypoint.sh"]

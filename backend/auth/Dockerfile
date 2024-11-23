FROM python:3 AS builder

COPY tools/requirements.txt .
RUN pip install --user -r requirements.txt && rm -f requirements.txt

FROM python:3-slim

RUN apt-get update && apt-get install -y libpq-dev dumb-init

ENV PYTHONUNBUFFERED 1
WORKDIR /app

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
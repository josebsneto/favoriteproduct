FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONOPTIMIZE=1 \
    PYTHONUNBUFFERED=1

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get clean \
    && apt-get install -y --no-install-recommends \
      build-essential \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt /tmp/requirements.txt

RUN pip install \
  --no-cache-dir \
  --upgrade \
  --require-hashes \
  -r /tmp/requirements.txt

COPY ./app /app

RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

CMD ["fastapi", "run", "app/entrypoints/fastapi/main.py"]

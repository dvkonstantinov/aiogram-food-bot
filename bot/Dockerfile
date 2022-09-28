FROM python:3.10-slim
WORKDIR /app

COPY . /app

RUN apt-get update && \
    apt-get install -yq tzdata && \
    ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

RUN pip install -r requirements.txt --no-cache-dir

CMD ["python3", "main.py"]
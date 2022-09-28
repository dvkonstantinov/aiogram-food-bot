FROM python:3.10-slim
WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY . /app
RUN pip3 install -r /app/requirements.txt --no-cache-dir

CMD ["gunicorn", "tgbot.wsgi:application", "--bind", "0:8000"]
#CMD ["python3", "manage.py", "runserver", "0:8000"]
FROM python:3.14-slim-bookworm

ENV PYTHONDONTWRITEBYCODE=1 \
    PYTHONBUNBUFFERED=1

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app .

CMD [ "python", "main.py" ]
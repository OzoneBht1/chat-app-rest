FROM python:3.11.0

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app/

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app/ 

RUN rm -rf ./scripts

COPY ./scripts/start /start

RUN chmod +x /start


EXPOSE 8000:8000

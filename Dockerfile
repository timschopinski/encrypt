FROM python:3.10-slim
MAINTAINER Tim Schopinski

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt

RUN pip3 install -r requirements.txt
RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN adduser user

USER user
CMD ["python main.py"]
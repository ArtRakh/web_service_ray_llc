FROM python:3.10-slim

COPY . /root

WORKDIR /root

RUN pip install flask gunicorn pandas pathlib joblib catboost pyarrow flask_wtf
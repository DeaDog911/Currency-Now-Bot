FROM python:3.7-slim

WORKDIR /botname

COPY requirements.txt /Currency-Now-Bot/
RUN pip install -r /Currency-Now-Bot/requirements.txt
COPY . /Currency-Now-Bot/

CMD python3 /Currency-Now-Bot/app.py

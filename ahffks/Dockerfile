FROM python:latest

WORKDIR /app/

COPY ./main.py /app/

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt

CMD uvicorn --host=127.0.0.1 --port 8000 main:app
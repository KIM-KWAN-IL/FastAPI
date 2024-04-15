FROM bitnami/python:3.10.5

RUN pip install --upgrade pip

WORKDIR /FASTAPI

COPY ./requirements.txt /FASTAPI/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /FASTAPI/requirements.txt

COPY ./app /FASTAPI/app

CMD ["uvicorn", "main:app". "--host" "0.0.0.0", "--port", "8000"]
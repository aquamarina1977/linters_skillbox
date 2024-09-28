FROM python:3.7.9-slim-stretch

RUN mkdir /app

COPY requirements.txt /app/

COPY app.py /app/

RUN python -m pip install -r /app/requirements.txt

WORKDIR /app

ENTRYPOINT ["python", "app.py"]
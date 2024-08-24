FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get install flask==3.0*
RUN apt-get update && apt-get install -y nano

RUN mkdir /app.py

COPY requirements.txt /app/

RUN python -m pip install -r /app.py/requirements.txt

COPY app.py /app/

WORKDIR /app

ENTRYPOINT ["python", "app.py"]
FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install python-pip -y
RUN apt-get install gunicorn -y

COPY requirements.txt requirements.txt
COPY flaskapp /opt/

RUN pip install -r requirements.txt

WORKDIR /opt/

CMD ["gunicorn","-b","0.0.0.0:8000","app:app","--workers=5"]


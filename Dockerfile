FROM python:3.8

EXPOSE 8000

WORKDIR /data/python/

COPY / ./

CMD ['./run.sh']

FROM python:3

WORKDIR /usr/src/app

RUN pip install --upgrade pip
RUN pip install requests
RUN pip install bs4

RUN pip install mysqlclient

CMD ["python","-u","__main__.py"]

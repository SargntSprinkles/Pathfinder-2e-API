FROM python:3.7-alpine

ADD . /app
WORKDIR /app

RUN pip install -r requirements.txt

CMD [ "python3", "api.py" ]
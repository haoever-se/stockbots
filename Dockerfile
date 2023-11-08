FROM python:3.9-slim-buster
WORKDIR /app
COPY ./requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_APP=./app/main.py
CMD ["flask", "run", "--host", "0.0.0.0"]
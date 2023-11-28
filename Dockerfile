FROM python:3.9.18-bookworm
WORKDIR /app
COPY ./requirements.txt /app
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_APP=./app/main.py
RUN flask db_create
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]
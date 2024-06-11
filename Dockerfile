FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -e .

EXPOSE 8000

CMD ["run-flask-app"]
from python:3.12.4

WORKDIR /app
COPY . /app/
RUN pip install poetry
RUN poetry install

CMD [ "make", "start" ]
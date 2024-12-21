from python:3.12.4

COPY . .
RUN pip install poetry
RUN poetry install

CMD [ "make", "start" ]
FROM python:3.8

WORKDIR /code
COPY ./requirements.txt /code
COPY ./requirements.in /code
RUN pip install -r /code/requirements.txt
RUN pip install -r /code/requirements.in
COPY ./app /code

EXPOSE 8010

CMD ["gunicorn", "--chdir", "foodgram", "--bind", ":8010", "foodgram.wsgi:application"]

FROM python:3.11.3-alpine

WORKDIR /code/

COPY . .

RUN pip install -r ./requirements.txt
RUN python3 manage.py makemigrations & python3 manage.py migrate

ENV PYTHONUNBUFFERED=1

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]

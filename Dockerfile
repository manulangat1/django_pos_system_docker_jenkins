FROM python:3.6 

RUN mkdir -p /code
WORKDIR /code 

RUN pip install -r requirementst.txt


COPY . /code 

EXPOSE 8000

CMD ["gunicorn","--chdir","backend",":8000","backend.wsgi:application",]
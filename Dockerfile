FROM python:3

WORKDIR /code

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . /code/ 

EXPOSE 8000
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

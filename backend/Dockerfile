FROM python:3.7-slim 
WORKDIR /app
COPY . .
RUN pip install -r /app/requirements.txt --no-cache-dir
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0:8000" ]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000" ]
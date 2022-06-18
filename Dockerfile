FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT=1 
# Ver esta parte

# Allows docker to cache installed dependencies between builds
COPY ./requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Adds our application code to the image
COPY . code
WORKDIR code

EXPOSE 8000

# Run the production server
CMD newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - ordermanagement.wsgi:application


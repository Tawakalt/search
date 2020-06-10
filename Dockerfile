# Base Image
FROM python:3-alpine

LABEL Name=search Version=0.0.1
EXPOSE 8000

# set working directory
WORKDIR /usr/src/app

# Setup and activate virtual enviroment
RUN pip install virtualenv
RUN virtualenv /venv
ENV VIRTUAL_ENV /venv
ENV PATH /venv/bin:$PATH

# Install project dependencies
COPY requirements.txt ./
RUN pip install -r requirements.txt

# copy project to working dir
COPY . .

# startup command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "search.wsgi"]

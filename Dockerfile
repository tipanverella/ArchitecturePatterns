FROM python:3.9-buster

# set working directory
WORKDIR /app

# install dependencies
COPY ./pyproject.toml /app
COPY ./poetry.lock /app
RUN pip install --no-cache-dir --upgrade poetry
RUN poetry update 

# copy current folder
COPY . /app
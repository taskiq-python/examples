FROM python:3.11-slim-buster

RUN pip install poetry==1.2.2

# Configuring poetry
RUN poetry config virtualenvs.create false

# Install gcc
RUN apt-get update \
    && apt-get install gcc libpq-dev -y

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install --without lint

# Copying actuall application
COPY . /app/src/
RUN poetry install --without lint

CMD ["gunicorn", "--worker-class", "aiohttp.GunicornWebWorker", "aiohttp_app.main:app", "-w", "1", "--bind", "0.0.0.0:8080"]
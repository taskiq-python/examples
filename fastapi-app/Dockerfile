FROM python:3.11-slim-buster

RUN pip install poetry==2.0.1

# Configuring poetry
RUN poetry config virtualenvs.create false

# Install gcc
RUN apt-get update \
    && apt-get install gcc libpq-dev -y

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install --without lint --no-root

# Copying actuall application
COPY . /app/src/
RUN poetry install --without lint

CMD ["uvicorn", "fastapi_app.__main__:get_app", "--factory", "--workers", "1", "--host", "0.0.0.0", "--port", "8080"]

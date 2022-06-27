FROM python:3.10 as prod
SHELL ["/bin/bash", "-c"]
RUN apt-get update -y && apt-get install -y default-mysql-client
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"
WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-dev
COPY . .
FROM prod as dev
RUN poetry install

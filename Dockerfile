FROM python:3.13-slim

WORKDIR /app

COPY poetry.lock pyproject.toml ./
RUN pip install poetry --root-user-action=ignore && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . ./

CMD ["poetry", "run", "main.py"]
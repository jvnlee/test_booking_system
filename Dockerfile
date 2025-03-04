FROM python:3.13.2

WORKDIR /app

COPY . .

RUN pip install poetry

RUN poetry config virtualenvs.create false && poetry install --no-root

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0"]
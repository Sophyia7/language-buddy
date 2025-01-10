FROM python:3.12 

WORKDIR /app 

RUN apt-get update && apt-get install -y --no-install-recommends \
  build-essential \
  && rm -rf /var/lib/apt/lists/* 


RUN pip install poetry 

COPY pyproject.toml poetry.lock ./ 

RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-ansi

COPY . . 

CMD ["python", "manage.py", "runserver", "0.0.0:8000"]


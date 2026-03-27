FROM public.ecr.aws/docker/library/python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements /app/requirements
RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r /app/requirements/dev.txt

COPY . /app

WORKDIR /app/apps/api

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
# FROM python:3.13-slim
FROM public.ecr.aws/docker/library/python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements /app/requirements
RUN pip install --no-cache-dir -r /app/requirements/watcher.txt

COPY . /app

WORKDIR /app

CMD ["python", "-m", "services.watcher.app.main"]
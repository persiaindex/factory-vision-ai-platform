FROM public.ecr.aws/docker/library/python:3.13-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements /app/requirements

RUN python -m pip install --upgrade pip \
    && python -m pip install --no-cache-dir -r /app/requirements/inference.txt \
    && python -m pip install --no-cache-dir -r /app/requirements/ml-docker.txt \
    && python -c "import torch, torchvision, cv2; print(torch.__version__); print(torchvision.__version__); print(cv2.__version__)"

COPY . /app

WORKDIR /app

CMD ["uvicorn", "services.inference.app.main:app", "--host", "0.0.0.0", "--port", "8001"]
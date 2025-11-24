# build stage
FROM python:3.11-slim AS builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y build-essential gcc libpq-dev --no-install-recommends && rm -rf /var/lib/apt/lists/*
COPY backend/requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip wheel -r requirements.txt -w /wheels

# final stage
FROM python:3.11-slim
RUN addgroup --system app && adduser --system --ingroup app app
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY --from=builder /wheels /wheels
RUN pip install --no-index --find-links=/wheels -r /wheels/../requirements.txt || true
COPY backend/ /app/
# collect static if you use WhiteNoise or similar
RUN mkdir -p /vol/static && chown -R app:app /vol
USER app
EXPOSE 8000
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--log-level", "info"]


#backend/Dockerfile
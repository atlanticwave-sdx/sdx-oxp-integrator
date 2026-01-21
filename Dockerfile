FROM python:3.11-slim-bullseye

WORKDIR /usr/src/app

# System deps commonly needed for uvloop/httptools wheels; keep minimal
RUN apt-get update \
  && apt-get install -y --no-install-recommends gcc python3-dev \
  && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY os-base/async-base/requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# App code
COPY topology-conversion/ /usr/src/app

EXPOSE 8000
ENTRYPOINT ["python3"]
CMD ["-m", "uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"]

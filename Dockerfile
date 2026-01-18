FROM python:3.11-slim-bullseye
LABEL description="NewsApp - Terminal News Browser"

# Install ca-certificates for SSL verification
RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

WORKDIR /app
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY src/ /app/src/
COPY config/ /app/config/
ENTRYPOINT ["/app/venv/bin/python", "-m", "src.main"]

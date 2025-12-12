FROM python:3.11

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use shell form so PORT expands
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}

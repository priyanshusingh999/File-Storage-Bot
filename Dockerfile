# Base image
FROM python:3.10-slim

# Working directory set karo
WORKDIR /app

# System dependencies install karo (agar required ho)
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies copy aur install karo
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Source code copy karo
COPY . .

# Environment variables ko runtime pe set karne ka option
# (Render ya Railway pe ye `.env` se aa jayenge)
ENV PORT=8080

# Bot ko run karo
CMD ["python", "main.py"]

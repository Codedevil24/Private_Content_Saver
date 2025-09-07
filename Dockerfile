FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# system deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg build-essential libc-dev git && \
    rm -rf /var/lib/apt/lists/*

# upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# python deps layer cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# copy source
COPY . .

# (optional) rename ytdl.txt → ytdl.py if cookies enabled
RUN if [ -f devgagan/modules/ytdl.txt ]; then \
        mv devgagan/modules/ytdl.txt devgagan/modules/ytdl.py; \
    fi

# non-root user
RUN useradd -m -s /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# run the actual package (repo ka main module)
CMD ["python3", "-m", "devgagan"]

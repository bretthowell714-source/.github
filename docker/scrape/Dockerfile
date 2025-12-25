FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

RUN apt-get update && apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      bash \
      gcc \
      g++ \
      make \
    && rm -rf /var/lib/apt/lists/*

COPY docker/scrape/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Optional-but-ready JS rendering (Chromium). This adds size, but avoids "it works on my machine"
# issues when you need rendered DOM scraping.
RUN python -m playwright install --with-deps chromium

WORKDIR /work
CMD ["/bin/bash"]

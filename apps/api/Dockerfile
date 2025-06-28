FROM python:3.11-slim

RUN groupadd osm && useradd osm -g osm 

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


COPY --chown=osm:osm requirements.txt* ./

RUN pip install -r requirements.txt

COPY --chown=osm:osm res/style /app/style
COPY --chown=osm:osm res/fonts /app/fonts
COPY --chown=osm:osm src /app/src

WORKDIR /app
USER osm

EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

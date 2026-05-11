FROM python:3.11-slim

RUN useradd -m -u 1000 appuser

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python scripts/generate_placeholders.py \
    && chmod +x docker/entrypoint.sh \
    && mkdir -p instance \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=5 \
    CMD python -c "import urllib.request as u; r=u.urlopen('http://127.0.0.1:8000/api/health'); assert r.getcode()==200" || exit 1

ENTRYPOINT ["/app/docker/entrypoint.sh"]

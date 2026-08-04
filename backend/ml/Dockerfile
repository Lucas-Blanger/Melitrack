FROM tensorflow/tensorflow:2.16.1

WORKDIR /app

COPY requirements.txt .

RUN grep -v "tensorflow" requirements.txt > /tmp/requirements.txt \
    && python -m pip install --no-cache-dir -r /tmp/requirements.txt \
    && python -c "import redis; print('redis-py', redis.__version__)"

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM python:3.9-slim

WORKDIR /app
COPY req.txt .
RUN pip install --upgrade pip && pip install -r req.txt
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

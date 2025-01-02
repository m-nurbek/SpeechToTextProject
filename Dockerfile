FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

ENV PYTHONUNBUFFERED=1

CMD ["streamlit", "run", "main.py", "--server.headless", "true"]
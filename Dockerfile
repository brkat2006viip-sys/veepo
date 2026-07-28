FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV DATABASE_URL=sqlite+aiosqlite:///./data/bot.db

RUN mkdir -p /app/data /app/uploads /app/temp /app/downloads /app/logs /app/reports

CMD ["python", "main.py"]

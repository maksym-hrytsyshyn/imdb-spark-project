FROM python:3.11

RUN apt-get update && apt-get install -y \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pyspark

WORKDIR /app

COPY . .

CMD ["python", "main.py"]

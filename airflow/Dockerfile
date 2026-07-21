FROM apache/airflow:3.3.0

USER root

RUN apt-get update && \
    apt-get install -y \
        default-jdk \
        procps \
        curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME=/usr/lib/jvm/default-java

USER airflow

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
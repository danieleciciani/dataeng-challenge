FROM apache/airflow:2.5.0
COPY requirements.txt /

USER root

# install linux dep

RUN apt-get update && \
    apt-get install -y software-properties-common && \
    rm -rf /var/lib/apt/lists/*

# Install OpenJDK-8
RUN apt update && \
    apt-get install -y openjdk-11-jdk && \
    apt-get install -y ant && \
    apt-get clean;

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME


USER airflow
# Install Python dependencies (Spark)
RUN pip install --no-cache-dir -r /requirements.txt
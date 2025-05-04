FROM bitnami/spark:latest
USER root

# Install Python packages if needed
RUN pip install pandas numpy

# Copy your application code
COPY src/spark-app.py /opt/bitnami/spark/spark-app.py

WORKDIR /opt/bitnami/spark
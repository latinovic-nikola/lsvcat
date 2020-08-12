FROM cluster-base

ARG SPARK_VERSION=2.4.5
ARG HADOOP_VERSION=2.7

# Spark Layer

RUN apt-get update -y && \
    apt-get install -y curl && \
    curl https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz -o spark.tgz && \
    tar -xf spark.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION} /usr/bin/ && \
    mkdir /usr/bin/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}/logs && \
    rm spark.tgz


# SPARK_HOME is the installed Apache Spark location used by the framework
# SPARK_MASTER_HOST is the master node hostname used by worker nodes to connect
# SPARK_MASTER_PORT is the master node port used by worker nodes to connect
# PYSPARK_PYTHON is the installed Python location used by Apache Spark to support its Python API


ENV SPARK_HOME /usr/bin/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}
ENV SPARK_MASTER_HOST spark-master
ENV SPARK_MASTER_PORT 7077
ENV PYSPARK_PYTHON python3



WORKDIR ${SPARK_HOME}
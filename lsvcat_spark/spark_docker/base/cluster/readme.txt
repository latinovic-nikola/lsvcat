Base image starting with Linux distribution and installing Java 8. *
Here we will also install pyhton distribution (3.7) for PySpark suppport and create a shared volume to simulate HDFS


* Apache Spark official GitHub repository has a dockerfile for Kubernetes deployment which uses a small debian image with a 
    built-in java 8 runtime environment (https://github.com/apache/spark/blob/master/resource-managers/kubernetes/docker/src/main/dockerfiles/spark/Dockerfile)





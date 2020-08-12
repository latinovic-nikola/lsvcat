FROM spark-base

ARG SPARK_MASTER_WEBUI_PORT=8080

EXPOSE ${SPARK_MASTER_WEBUI_PORT} ${SPARK_MASTER_PORT}
CMD bin/spark-class org.apache.spark.deploy.master.Master >> logs/spark-master.out
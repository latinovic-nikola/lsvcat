FROM spark-base

# -- Runtime

ARG SPARK_WORKER_WEBUI_PORT=8081

EXPOSE ${SPARK_WORKER_WEBUI_PORT}
CMD bin/spark-class org.apache.spark.deploy.worker.Worker spark://${SPARK_MASTER_HOST}:${SPARK_MASTER_PORT} >> logs/spark-worker.out
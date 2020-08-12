FROM cluster-base

# Add pyspark and jupyterlab layer


ARG pyspark_version=2.4.6
ARG jupyterlab_version=2.1.5

COPY jupyter/notebooks/ ${SHARED_WORKSPACE}

RUN apt-get update -y && \
    apt-get install -y python3-pip && \
    pip3 install pyspark==${pyspark_version} jupyterlab==${jupyterlab_version}


EXPOSE 8888
WORKDIR ${SHARED_WORKSPACE}
CMD jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=
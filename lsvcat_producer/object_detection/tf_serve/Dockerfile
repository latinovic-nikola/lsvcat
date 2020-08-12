FROM tensorflow/serving

MAINTAINER "Nikola Latinovic"

LABEL version="0.0.1"
LABEL description="Deploy tensorflow models to docker serving image"

RUN apt-get clean


ADD ./models /models
ADD ./config/model_config /models/model_config

EXPOSE 8500
EXPOSE 8501

ENTRYPOINT ["tensorflow_model_server", "--model_config_file=/models/model_config", "--port=8500", "--rest_api_port=8501"]

$SPARK_VERSION_NUMBER = "2.4.5"
$HADOOP_VERSION_NUMBER = "2.7"


#iex "docker build -f base\cluster\.dockerfile -t cluster-base ."
#iex "docker build --build-arg spark_version=$SPARK_VERSION --build-arg hadoop_version=$HADOOP_VERSION -f base\spark\.dockerfile -t spark-base ."
#iex "docker build -f master\.dockerfile -t spark-master ."
#iex "docker build -f worker\.dockerfile -t spark-worker ."
iex "docker build -f jupyter\.dockerfile -t spark-jupyter ."
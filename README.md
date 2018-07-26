### web启动命令
```

uwsgi --master --http :5000 --process 4 --http-websockets --wsgi app:app
```
### spark启动命令
```
 spark-submit    \
 --name "face"    \ 
 --master yarn \
 --deploy-mode client\  
 --conf "spark.yarn.appMasterEnv.SPARK_HOME=$SPARK_HOME"     \
 --conf "spark.yaDDrn.appMasterEnv.PYSPARK_PYTHON=$PYSPARK_PYTHON"\     
 --archives hdfs:///user/kenwood/src   \
 pyspark_main.py 
```
### bug
```
import cv2 报错　Error while loading shared libraries: libgthread-2.0.so.0”。
apt-get install libglib2.0-0
apt-get install libsm6
apt-get install libxrender1
apt-get install libxext-dev
```
### docker 
```
# 下载docker镜像
zookeeker: docker pull zookeeper:latest
kafka: docker pull wurstmeister/kafka:latest

#启动zookeeper
docker run -d --name zookeeper --publish 2181:2181 \
--volume /etc/localtime:/etc/localtime \
zookeeper:latest
#启动kafka
docker run -d --name kafka --publish 9092:9092 \
--link zookeeper \
--env KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181 \
--env KAFKA_ADVERTISED_HOST_NAME=kafka所在宿主机的IP \
--env KAFKA_ADVERTISED_PORT=9092 \
--volume /etc/localtime:/etc/localtime \
wurstmeister/kafka:latest

```
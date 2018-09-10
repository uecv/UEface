

## 启动mysql
mysql_install_db --user=root
mysqld --user=root &

## 初始化数据库
mysql -u root < /build/UEface/docker/initdb.sql
python3 /build/UEface/ueface.py initdb


## 初始化图像库
python3 /build/UEface/ueface.py build


## 启动流媒体服务器
ffserver -f /build/UEface/docker/ffserver.conf &

## 启动redis
redis-server /build/lib/redis/redis.conf


## 启动web后台
python3 /build/UEface/ueface.py web &



## 启动web
rm -f /build/lib/nginx/conf/nginx.conf
cp -f /build/UEface/docker/nginx.conf /build/lib/nginx/conf/
/build/lib/nginx/sbin/nginx -c /build/lib/nginx/conf/nginx.conf


# docker cp wy.mp4 face2:/build/wy.mp4

#docker run -it --name face2 -p 80:80 -p 5000:5000 -v /root/ueface/UEface:/build/UEface face:v1.1
# ffmpeg -i /build/wy.mp4 "http://localhost:8888/feed1.ffm"


# docker cp UEface/docker/nginx.conf face2:/build/UEface/docker/nginx.conf
# docker cp UEface/src/procesor.py face2:/build/UEface/src/procesor.py
# docker cp UEface/settings.py face2:/build/UEface/settings.py


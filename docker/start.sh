## 启动mysql
service mysqld start

## 初始化数据库
python3 /build/UEface/ueface.py initdb


## 启动流媒体服务器
ffserver -f /build/UEface/docker/ffserver.conf

## 启动redis
redis-server /build/lib/redis/redis.conf


## 启动web后台
python3 /build/UEface/ueface.py web


## 启动web
nginx -c /build/UEface/nginx.conf
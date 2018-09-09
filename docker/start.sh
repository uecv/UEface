

## 启动mysql
mysqld --initialize --user=mysql --basedir=/data/mysql/installdir --datadir=/data/mysql/datadir/3306/data

## 初始化数据库
python3 /build/UEface/ueface.py initdb


## 启动流媒体服务器
ffserver -f /build/UEface/docker/ffserver.conf

## 启动redis
redis-server /build/lib/redis/redis.conf


## 启动web后台
python3 /build/UEface/ueface.py web


## 启动web
cp -f  /build/UEface/docker/nginx.conf /build/lib/nginx/conf/nginx.conf
/build/lib/nginx/sbin/nginx -c /build/lib/nginx/conf/nginx.conf


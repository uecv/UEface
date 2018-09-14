source_url = $1

## 启动mysql
#mysql_install_db --user=root &&  mysqld_safe  --user=root &



## 初始化数据库,初始化图像库
mysql -u root < /build/UEface/docker/initdb.sql && \
python3 /build/UEface/ueface.py initdb && \
python3 /build/UEface/ueface.py build



## 启动流媒体服务器
ffserver -f /build/UEface/docker/ffserver.conf &


## 启动redis
redis-server /build/lib/redis/redis.conf


## 启动web后台
nohup python3 /build/UEface/ueface.py web > web.nohup &


## 启动web
rm -f /build/lib/nginx/conf/nginx.conf && \
cp -f /build/UEface/docker/nginx.conf /build/lib/nginx/conf/ && \
/build/lib/nginx/sbin/nginx -c /build/lib/nginx/conf/nginx.conf


#nohup python3 /build/UEface/ueface.py web > web.nohup &
#nohup python3 /build/UEface/ueface.py main "rtsp://admin:qwe123456@192.168.1.202:554/cam/realmonitor?channel=1&subtype=0" > main.nohup &
#nohup python3 /build/UEface/ueface.py main > main.nohup &






### docker单机版 

#### 1.构建docker镜像离线文件准备
创建一个目录face,目录下准备好以下内容：
ffmpeg_packages： ffmpeg的依赖源码包  
Python-3.6.6.tgz： python的源码包
build-ffmpeg.sh： ffmpeg离线安装脚本,该脚本在UEface/docker文件夹里面
UEface:  项目源码
app:  打包后的WEBface的app代码文件

#### 2.构建镜像
进入face目录,运行下面的命令
```
docker build -f Dockerfile.ueface -t face:v0.7 .
```
#### 3.启动容器
```
docker run -it --name face3 -p:80:80 -p 5000:5000 \
 -v /root/ueface/UEface/src/library/images/:/build/UEface/src/library/images/ \
 face:v0.7 bash

注意： 
(1)目前版本映射的端口只能是80以及5000, 
(2)images目录格式需要按照特定的格式放置,图片名字也是.

```


#### 4.进入容器启动服务
(1) 启动mysql
```
mysql_install_db --user=root &&  mysqld_safe  --user=root &
```
(2) 初始化脚本
```
sh /build/UEface/docker/start.sh
```
(3) 推流 & 开始识别视频流
```
sh /build/UEface/docker/push_stream.sh rtsp协议的视频流地址
例如：
sh /build/UEface/docker/push_stream.sh "rtsp://admin:qwe123456@192.168.1.202:554/cam/realmonitor?channel=1&subtype=0"
```
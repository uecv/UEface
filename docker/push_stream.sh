#!/usr/bin/env bash

source_url=$1
echo $source_url
# 推流
nohup ffmpeg  -r 25  -rtsp_transport tcp -i "$source_url" "http://localhost:8888/feed1.ffm" > ffmpeg.nohup &
# 处理结果
nohup python3 /build/UEface/ueface.py main $source_url > main.nohup &
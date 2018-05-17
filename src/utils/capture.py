#!/usr/bin/env python
# coding: utf-8
"""
   @author: kenwood
   @time: 18-5-17 上午11:59
"""
import subprocess as sp


"""
this module is push liv stream to ffmpeg ,then to nginx
hls,rtmp live stream module
"""


def stream_live(frame):
    height, width, ch = frame.shape

    ffmpeg = 'ffmpeg'
    dimension = '{}x{}'.format(width, height)
    f_format = 'bgr24'  # remember OpenCV uses bgr format
    # fps = str(cap.get(cv2.CAP_PROP_FPS))
    fps = '60'
    rtmp_addres = 'rtmp://localhost/vod'
    hls_addres = "rtmp://localhost/hls/demo"
    flv_addres = 'rtmp://localhost/live/livestream'

    # hls command
    # ffmpeg -re  -i output_file_name.mp4 -vcodec libx264  -acodec aac -strict
    # -2 -f flv rtmp://localhost/hls/demo

    ###command for rtmp stream###
    command1 = [ffmpeg,
                '-y',
                '-f', 'rawvideo',
                '-vcodec', 'rawvideo',
                '-s', dimension,
                '-pix_fmt', 'bgr24',
                '-r', fps,
                '-i', '-',  # The imput comes from a pipe
                '-an',
                '-b:v', '5000k',
                '-f', 'flv',
                rtmp_addres]

    """command for hls stream """

    command2 = [ffmpeg,
                '-y',
                '-f', 'rawvideo',
                # '-vcodec','rawvideo',
                '-pix_fmt', 'bgr24',
                '-r', fps,
                '-s', dimension,
                '-i', '-',
                '-c:v', 'libx264',
                '-pix_fmt', 'yuv420p',
                # '-preset', 'ultrafast',
                '-b:v', '5000k',
                '-f', 'flv',
                flv_addres]

    # with open("stderr.txt", "wb") as err, open('stdout.txt', 'wb') as out:
    proc = sp.Popen(command2, stdin=sp.PIPE, stdout=sp.PIPE, stderr=sp.PIPE)

    while True:
        # write frame to the stdin pipeline
        proc.stdin.write(frame.tostring())


    proc.stdin.close()
    proc.stderr.close()
    proc.wait()

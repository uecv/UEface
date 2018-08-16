# coding=utf-8
"""
   @author: wy
   @time: 2018/7/30 0030
"""
import sys

def help():
    print("useage: python ueface web")
    print("useage: python ueface main")
    print("useage: python ueface initdb")
def main():
    try:
        cmd = sys.argv[1]
    except IndexError as e:
        print("option error")
        sys.exit()
    if cmd == 'main':
        from src import procesor
        procesor.process()
    elif cmd == 'web':
        from src import tnado_app as web
        web.main()
    elif cmd == 'initdb':
        from src.storage import initdb
        initdb.init()
    elif cmd == 'build':
        from src.FaceFeature import BuildFaceNetLib as bfn
        bfn.build()
    else:
        help()
if __name__ == '__main__':
    main()
# coding=utf-8
"""
   @author: wy
   @time: 2018/7/30 0030
"""
import sys
from script import init
import tnado_app as web
import procesor

def help():
    print("useage: python ueface web")
    print("useage: python ueface main")
    print("useage: python ueface initdb")
def main():
    try:
        cmd = sys.argv[1]
    except IndexError  as e:
        print("option error")
        sys.exit()
    if cmd == 'main':
        procesor.process()
    elif cmd == 'web':
        web.main()
    elif cmd == 'initdb':
        init.intidb()
    else:
        help()
if __name__ == '__main__':
    main()
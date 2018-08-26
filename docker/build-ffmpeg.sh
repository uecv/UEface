#!/bin/bash

# https://github.com/markus-perl/ffmpeg-build-script

VERSION=1.0
CWD=$(pwd)
# package中需要预先放好ffmpeg依赖的包
PACKAGES="$CWD/ffmpeg_packages"
TMP_PACKAGES="$CWD/tmp_ffmpeg_packages"
WORKSPACE="$CWD/ffmpeg"
CC=clang
LDFLAGS="-L${WORKSPACE}/lib -lm"
CFLAGS="-I${WORKSPACE}/include"
PKG_CONFIG_PATH="${WORKSPACE}/lib/pkgconfig"

# Speed up the process
# Env Var NUMJOBS overrides automatic detection
if [[ -n $NUMJOBS ]]; then
    MJOBS=$NUMJOBS
elif [[ -f /proc/cpuinfo ]]; then
    MJOBS=$(grep -c processor /proc/cpuinfo)
elif [[ "$OSTYPE" == "darwin"* ]]; then
	MJOBS=$(sysctl -n machdep.cpu.thread_count)
else
    MJOBS=4
fi

make_dir () {
	if [ ! -d $1 ]; then
		if ! mkdir $1; then
			printf "\n Failed to create dir %s" "$1";
			exit 1
		fi
	fi
}

remove_dir () {
	if [ -d $1 ]; then
		rm -r "$1"
	fi
}

download () {
	if [ ! -f "$PACKAGES/$2" ]; then

		echo "Downloading $1"
		curl -L --silent -o "$PACKAGES/$2" "$1"

		EXITCODE=$?
		if [ $EXITCODE -ne 0 ]; then
			echo ""
			echo "Failed to download $1. Exitcode $EXITCODE. Retrying in 10 seconds";
			sleep 10
			curl -L --silent -o "$PACKAGES/$2" "$1"
		fi

		EXITCODE=$?
		if [ $EXITCODE -ne 0 ]; then
			echo ""
			echo "Failed to download $1. Exitcode $EXITCODE";
			exit 1
		fi

		echo "... Done"

		if ! tar -xvf "$PACKAGES/$2" -C "$PACKAGES" 2>/dev/null >/dev/null; then
			echo "Failed to extract $2";
			exit 1
		fi

	fi
}



extract () {
		if ! tar -xvf "$PACKAGES/$1" -C "$TMP_PACKAGES" 2>/dev/null >/dev/null; then
			echo "Failed to extract $2";
			exit 1
		fi
        echo "extract Done"
}



execute () {
	echo "$ $*"

	OUTPUT=$($@ 2>&1)

	if [ $? -ne 0 ]; then
        echo "$OUTPUT"
        echo ""
        echo "Failed to Execute $*" >&2
        exit 1
    fi
}

build () {
	echo ""
	echo "building $1"
	echo "======================="

	if [ -f "$TMP_PACKAGES/$1.done" ]; then
		echo "$1 already built. Remove $TMP_PACKAGES/$1.done lockfile to rebuild it."
		return 1
	fi

	return 0
}

command_exists() {
    if ! [[ -x $(command -v "$1") ]]; then
        return 1
    fi

    return 0
}


build_done () {
	touch "$TMP_PACKAGES/$1.done"
}

echo "ffmpeg-build-script v$VERSION"
echo "========================="
echo ""

case "$1" in
"--cleanup")
	remove_dir $TMP_PACKAGES
	remove_dir $WORKSPACE
	echo "Cleanup done."
	echo ""
	exit 0
    ;;
"--build")

    ;;
*)
    echo "Usage: $0"
    echo "   --build: start building process"
    echo "   --cleanup: remove all working dirs"
    echo "   --help: show this help"
    echo ""
    exit 0
    ;;
esac

echo "Using $MJOBS make jobs simultaneously."


if [ ! -d "$PACKAGES" ]; then
	echo "$PACKAGES don't exist!"
	return 1
fi


# make_dir $PACKAGES
make_dir $WORKSPACE
make_dir $TMP_PACKAGES

export PATH=${WORKSPACE}/bin:$PATH


if ! command_exists "make"; then
    echo "make not installed.";
    exit 1
fi

if ! command_exists "g++"; then
    echo "g++ not installed.";
    exit 1
fi

if ! command_exists "curl"; then
    echo "curl not installed.";
    exit 1
fi


if build "yasm"; then
	#download "http://www.tortall.net/projects/yasm/releases/yasm-1.3.0.tar.gz" "yasm-1.3.0.tar.gz"
	extract "yasm-1.3.0.tar.gz"
	cd $TMP_PACKAGES/yasm-1.3.0 || exit
	execute ./configure --prefix=${WORKSPACE}
	execute make -j $MJOBS
	execute make install
	build_done "yasm"
fi

if build "nasm"; then
	#download "http://www.nasm.us/pub/nasm/releasebuilds/2.13.03/nasm-2.13.03.tar.gz" "nasm.tar.gz"
	extract "nasm-2.13.03.tar.gz"
	cd $TMP_PACKAGES/nasm-2.13.03 || exit
	execute ./autogen.sh
	execute ./configure --prefix=${WORKSPACE} --disable-shared --enable-static
	execute make -j $MJOBS
	execute make install
	build_done "nasm"
fi


if build "x264"; then
    #download "http://ftp.videolan.org/pub/x264/snapshots/x264-snapshot-20180531-2245.tar.bz2" "last_x264.tar.bz2"
	#curl -L --silent -o "$PACKAGES/last_x264.tar.bz2" "http://ftp.videolan.org/pub/x264/snapshots/x264-snapshot-20180531-2245.tar.bz2"
	#git clone --depth 1 http://git.videolan.org/git/x264 "$PACKAGES/last_x264"
	#tar -xvf "$PACKAGES/last_x264.tar.bz2" -C "$PACKAGES" 2>/dev/null >/dev/null;
	extract "x264-snapshot-20180531-2245.tar.bz2"
	cd $TMP_PACKAGES/x264-snapshot-20180531-2245 || exit
    execute ./configure --prefix=${WORKSPACE} --enable-static
    execute make -j $MJOBS
	execute make install
	build_done "x264"
fi



if build "x265"; then
	#download "https://bitbucket.org/multicoreware/x265/downloads/x265_2.8.tar.gz" "x265-2.8.tar.gz"
	extract "x265-2.8.tar.gz"
	cd $TMP_PACKAGES/x265_2.8 || exit
	cd source || exit
	execute cmake -DCMAKE_INSTALL_PREFIX:PATH=${WORKSPACE} -DENABLE_SHARED:bool=off .
	execute make -j $MJOBS
	execute make install
	sed "s/-lx265/-lx265 -lstdc++/g" "$WORKSPACE/lib/pkgconfig/x265.pc" > "$WORKSPACE/lib/pkgconfig/x265.pc.tmp"
	mv "$WORKSPACE/lib/pkgconfig/x265.pc.tmp" "$WORKSPACE/lib/pkgconfig/x265.pc"
	build_done "x265"
fi


if build "fdk_aac"; then
	#download "http://downloads.sourceforge.net/project/opencore-amr/fdk-aac/fdk-aac-0.1.6.tar.gz?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fopencore-amr%2Ffiles%2Ffdk-aac%2F&ts=1457561564&use_mirror=kent" "fdk-aac-0.1.6.tar.gz"
	extract "fdk-aac-0.1.6.tar.gz"
	cd $TMP_PACKAGES/fdk-aac-0.1.6 || exit
	execute ./configure --prefix=${WORKSPACE} --disable-shared --enable-static
	execute make -j $MJOBS
	execute make install
	build_done "fdk_aac"
fi


if build "lame"; then
	#download "http://kent.dl.sourceforge.net/project/lame/lame/3.100/lame-3.100.tar.gz" "lame-3.100.tar.gz"
	extract "lame-3.100.tar.gz"
	cd $TMP_PACKAGES/lame-3.100 || exit
	execute ./configure --prefix=${WORKSPACE} --disable-shared --enable-static --enable-nasm
	execute make -j $MJOBS
	execute make install
	build_done "lame"
fi



if build "libopus"; then
	#download "https://archive.mozilla.org/pub/opus/opus-1.2.1.tar.gz" "opus-1.2.1.tar.gz"
	extract "opus-1.2.1.tar.gz"
	cd $TMP_PACKAGES/opus-1.2.1 || exit
	execute ./configure --prefix=${WORKSPACE} --disable-shared
	execute make -j $MJOBS
	execute make install
	build_done "libopus"
fi


if build "libogg"; then
	#download "http://downloads.xiph.org/releases/ogg/libogg-1.3.3.tar.gz" "libogg-1.3.3.tar.gz"
	extract "libogg-1.3.3.tar.gz"
	cd $TMP_PACKAGES/libogg-1.3.3 || exit
	execute ./configure --prefix=${WORKSPACE} --disable-shared --enable-static
	execute make -j $MJOBS
	execute make install
	build_done "libogg"
fi


if build "libvorbis"; then
	#download "http://downloads.xiph.org/releases/vorbis/libvorbis-1.3.6.tar.gz" "libvorbis-1.3.6.tar.gz"
	extract "libvorbis-1.3.6.tar.gz"
	cd $TMP_PACKAGES/libvorbis-1.3.6 || exit
	execute ./configure --prefix=${WORKSPACE} --enable-static --disable-shared
	execute make -j $MJOBS
	execute make install
	build_done "libvorbis"
fi

if build "libvpx"; then
    #mkdir $PACKAGES/libvpx
    #git clone --depth 1 https://github.com/webmproject/libvpx.git $PACKAGES/libvpx
    # libvpx-1.7.0.tar.gz 在centos6会报错，centos7没有问题
    extract "libvpx-1.5.0.tar.gz"
    cd $TMP_PACKAGES/libvpx-1.5.0 || exit
	execute ./configure --prefix=${WORKSPACE} --disable-examples --disable-unit-tests --enable-vp9-highbitdepth --as=yasm
	execute make -j $MJOBS
	execute make install
	build_done "libvpx"
fi


if build "ffmpeg"; then
    #download "http://ffmpeg.org/releases/ffmpeg-3.4.4.tar.bz2" "ffmpeg-snapshot.tar.bz2"
    extract "ffmpeg-3.4.4.tar.bz2"
    cd $TMP_PACKAGES/ffmpeg-3.4.4 || exit
    PKG_CONFIG_PATH="$WORKSPACE/lib/pkgconfig" ./configure \
      --prefix="$HOME/ffmpeg_build" \
      --pkg-config-flags="--static" \
      --extra-cflags="-I$WORKSPACE/include" \
      --extra-ldflags="-L$WORKSPACE/lib" \
      --extra-libs=-lpthread \
      --extra-libs=-lm \
      --bindir="$WORKSPACE/bin" \
      --enable-gpl \
      --enable-libfdk_aac \
      --enable-libfreetype \
      --enable-libmp3lame \
      --enable-libopus \
      --enable-libvorbis \
      --enable-libvpx \
      --enable-libx264 \
      --enable-libx265 \
      --enable-nonfree
    execute make -j $MJOBS
    execute make install
fi

INSTALL_FOLDER="/usr/bin"
if [[ "$OSTYPE" == "darwin"* ]]; then
INSTALL_FOLDER="/usr/local/bin"
fi

echo ""
echo "Building done. The binary can be found here: $WORKSPACE/bin/ffmpeg"
echo ""


cp "$WORKSPACE/bin/ffmpeg" "$INSTALL_FOLDER/ffmpeg"
cp "$WORKSPACE/bin/ffserver" "$INSTALL_FOLDER/ffserver"
echo "Done. ffmpeg is now installed to your system"

exit 0
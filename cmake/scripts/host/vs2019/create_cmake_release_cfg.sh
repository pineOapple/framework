#!/bin/sh
counter=0
while [ ${counter} -lt 5 ]
do
	cd ..
	if [ -f "cmake_build_config.py" ];then
		break
	fi
	counter=$((counter=counter + 1))
done

if [ "${counter}" -ge 5 ];then
	echo "create_cmake_cfg.sh not found in upper directories!"
	exit 1
fi

build_generator=""
os_fsfw="host"
builddir="Release-VS2019"

if [ "${OS}" = "Windows_NT" ]; then
	build_generator="Visual Studio 16 2019"
# Could be other OS but this works for now.
else
	build_generator="Unix Makefiles"
fi

python3 cmake_build_config.py -o "${os_fsfw}" -g "${build_generator}" -b "release" -l "${builddir}"

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

build_generator="Unix Makefiles"
os_fsfw="linux"
builddir="build-Release"

echo "Running command (without the leading +):"
set -x # Print command 
python3 cmake_build_config.py -o "${os_fsfw}" -g "${build_generator}" -b "reldeb" \
	-t "host/none" -l "${builddir}"
# Use this if commands are added which should not be printed
# set +x

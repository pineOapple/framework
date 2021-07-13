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
builddir="build-Debug"
build_generator="Ninja"
if [ "${OS}" = "Windows_NT" ]; then
    python="py"
# Could be other OS but this works for now.
else
    python="python3"
fi

echo "Running command (without the leading +):"
set -x # Print command 
"${python}" cmake_build_config.py -o "${os_fsfw}" -g "${build_generator}" -b "debug" -l "${builddir}"
# Use this if commands are added which should not be printed
# set +x

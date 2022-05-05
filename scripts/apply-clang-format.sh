#!/bin/bash
if [[ ! -f README.md ]]; then
	cd ..
fi

find ./bsp_hosted -iname *.h -o -iname *.cpp -o -iname *.c | xargs clang-format --style=file -i
find ./example_common -iname *.h -o -iname *.cpp -o -iname *.c | xargs clang-format --style=file -i

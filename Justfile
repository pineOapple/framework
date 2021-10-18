python_script := './cmake/scripts/cmake-build-cfg.py'
default_host_os := if os_family() == "linux" { "linux" } else { "host" }

# Build host-debug-ninja target
default: debug-ninja

# Build for Host with Debug configuration and the Make build system
debug-make:
	{{python_script}} -o {{default_host_os}} -l build-Debug -g "make"

# Build for Host with Debug configuration and the Ninja build system
debug-ninja:
	{{python_script}} -o {{default_host_os}} -l build-Debug -g "ninja"

# Build for Host with Release configuration and the Make build system
release-make:
	{{python_script}} -b release -o {{default_host_os}} -l build-Release -g "make"

# Build for Host with Release configuration and the Ninja build system
release-ninja:
	{{python_script}} -b release -o {{default_host_os}} -l build-Release -g "ninja"
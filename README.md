<img align="center" src=doc/images/FSFW_Logo_V3_bw.png width="50%">

# <a id="top"></a> <a name="linux"></a> FSFW Example Application

This repository features a demo application. The example has been run successfully on the following 
platforms:

 - Linux host machine with the Linux OSAL or the Host OSAL
 - Windows with the Host OSAL
 - STM32H743ZI-Nucleo with the FreeRTOS OSAL
 - Raspberry Pi with the Linux OSAL
 - STM32H743ZI-Nucleo with the RTEMS OSAL
 
The purpose of this example is to provide a demo of the FSFW capabilities.
However, it can also be used as a starting point to set up a repository for
new flight software. It also aims to provide developers with practical examples
of how the FSFW is inteded to be used and how project using the FSFW should or can be
set up and it might serve as a basic test platform for the FSFW as well to ensure all OSALs
are compiling and running as expected.

The repository contains a Python TMTC program which can be used to showcase
the TMTC capabilities of the FSFW (currently, using the ECSS PUS packet standard).

# Configuring the Example

The build system will copy three configuration files into the build directory:

1. `commonConfig.h` which contains common configuration parameters
2. `OBSWConfig.h` which can contain machine and architecture specific configuration options
3. `FSFWConfig.h` which contains the configuration for the flight software framework

These files can be edited manually after `CMake` build generation.

# Index

[Getting started with Eclipse for C/C++](example_common/doc/README-eclipse.md#top)<br>
[Getting started with CMake](example_common/doc/README-cmake.md#top)<br>

[Getting started with the Hosted OSAL](#this)<br>
[Getting started with the FreeRTOS OSAL on a STM32](https://egit.irs.uni-stuttgart.de/fsfw/fsfw-example-stm32h7-freertos)<br>
[Getting started with the RTEMS OSAL on a STM32](https://egit.irs.uni-stuttgart.de/fsfw/fsfw-example-stm32h7-rtems)<br>
[Getting started with the Raspberry Pi](https://egit.irs.uni-stuttgart.de/fsfw/fsfw-example-linux-mcu)<br>
[Getting started with the Beagle Bone Black](https://egit.irs.uni-stuttgart.de/fsfw/fsfw-example-linux-mcu)<br>

# <a id="this"></a> FSFW demo with Host OSAL on Windows or Linux

This demo has been tested for Windows and Linux. It uses 
the host abstraction layer of the FSFW.

## General Information

This demo provides the opportunity to to test functionality of the
FSFW on a host computer without the need of setting up external embedded hardware.

## Prerequisites
1. Makefile build: make installed (bundled with MSYS2 on Windows or via [xPacks Windows Build Tools](https://xpack.github.io/windows-build-tools/install/)). Natively installed on Linux.
2. Recommended for application code development: [Eclipse for C/C++](https://www.eclipse.org/downloads/packages/) . 
   Project files and launch configuration are provided for Eclipse to ease development.
   Visual Studio support might follow soon following CMake implementation.
3. CMake Build: Correct CMake installation.

### Windows - MinGW64 build

1. [MSYS2 and MinGW64](https://www.msys2.org/) installed
2. Update MSYS2 by opening it and running
   ```sh
   pacman -Syuuu
   ```
   
   After that, the gcc toolchain, git, make and CMake should be installed with
   ```sh
   pacman -S git mingw-w64-x86_64-gcc mingw-w64-x86_64-gdb mingw-w64-x86_64-make mingw-w64-x86_64-cmake
   ```
   
   You can install a full development environment with
   ```sh
   pacman -S base-devel
   ```

   or install `gcc`, `gdb` and `mingw32-make` with the following command 

   ```sh
   pacman -S mingw-w64-x86_64-toolchain
   ```
   
   It is recommended to set up aliases to get to the example directory
   quickly.
   
3. It is recommended to add the MinGW64 bit binaries to the system path so Eclipse can use 
   them. It is also recommended to run `git config --global core.autocrlf true` when using MinGW64 
   to have consistent line endings on Windows systems.
   
### Linux - Enabling RTOS functionalities

The last chapter in the [Linux README](README-linux.md#top) specifies some steps required
to cleanly run the FSFW on a (host) Linux system.

## Building the Software with CMake

CMake should be [installed](https://cmake.org/install/) first.
More detailed information on the CMake build process and options
can be found in the [CMake README](README-cmake.md#top).
Readers unfamiliar with CMake should read this first. The following steps will show to to build
the Debug executable using either the "Unix Makefiles" generator on Linux or
the "MinGW Makefiles" generator in Windows in the command line to be as generic as possible.

### Linux Build

1. Create a new folder for the executable.
   ```sh
   mkdir Debug
   cd Debug
   ```
   
2. Configure the build system 
   ```sh
   cmake -G "Unix Makefiles" -DCMAKE_BUILD_TYPE=Debug -DOS_FSFW=host ..
   ```
   
3. Build the software
   ```sh
   cmake --build . -j
   ```

4. The binary will be located inside the Debug folder and can be run there
   ```sh
   ./fsfw-example
   ```
   
### MinGW64 Build

Set up MinGW64 like explained previously. 

The CMake build can be generated either with the CMake GUI tool or with the MinGW64 command line.
Steps will be shown with the MinGW64 command line tool, but the CMake GUI can be used on Windows 
as well to have a convenient way to configure the CMake build.

1. Open the MinGW64 terminal and navigate to the `fsfw_example` folder
2. Create a new folder for the executable.
   ```sh
   mkdir Debug
   cd Debug
   ```
	
   The build options can be displayed with `cmake -L` . 
   
3. Configure the project and generate the native MinGW64 buildsystem
   ```sh
   cmake -G "MinGW Makefiles" -DCMAKE_BUILD_TYPE=Debug -DOS_FSFW=host ..
   ```
   
   The build configuration can also be performed with the shell scripts located
   inside `cmake/scripts/Host` or the Python helper script `cmake_build_config.py`
   inside `cmake/scripts`. The configured build options can now be shown with `cmake -L`.

4. Call the build system (Make)
   ```
   cmake --build . -j
   ```
  
5. Like already mentioned, it is recommended to run the binary directly as an executable by 
   double-clicking it or in the Windows Terminal. 
   
### Setting up Eclipse for CMake projects

The separate [Eclipse README](README-eclipse#top) specifies how to set up Eclipse to build CMake projects. 
Separate project files and launch configurations for the MinGW build were provided.
  
## Building the Software with Makefiles

The Makefile is able to determine the OS and supply additonal required libraries, 
but this has only been tested for Windows 10 and Linux (Ubuntu 20.04)

1. Clone this repository
   ```sh
   git clone https://egit.irs.uni-stuttgart.de/fsfw/fsfw_example.git
   ```

2. Set up submodules
   ```sh
   git submodule init
   git submodule update
   ```

3. Copy the `Makefile-Hosted` file in the `make` folder into the cloned folder root
   and rename it to `Makefile`
   
4. Once all the prerequisites have been met. the binary can be built with the following command. 
   Replace `debug` with `release` to build the optimized binary.

   ```sh
   make debug -j
   ```
   
### Setting up Eclipse for CMake projects

The separate [Eclipse README](README-eclipse#top) specifies how to set up Eclipse to build CMake
projects. Separate project files and launch configurations for the MinGW build were provided.
The debug output is colored by default. It is recommended to install the
`ANSI Escape in Console` plugin in Eclipse so the coloring works in the Eclipse console.


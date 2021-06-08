# FSFW demo with Host OSAL on Windows or Linux

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
   
   The build configuration can also be performed with the shell scripts located inside `cmake/scripts/Host` or the Python helper script `cmake_build_config.py` inside `cmake/scripts`.
   The configured build options can now be shown with `cmake -L`.

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

The separate [Eclipse README](README-eclipse#top) specifies how to set up Eclipse to build CMake projects. Separate project files and launch configurations for the MinGW build were provided. The debug output is colored by default. It is recommended to install the
`ANSI Escape in Console` plugin in Eclipse so the coloring works in the Eclipse console.


## Running or Debugging the Software - Makefile

### Linux 
The Makefile binary will be generated in the `_bin` folder and can be run in Linux directly from the console.

### Windows
On Windows, it is recommended to run the binary in the command line or as a regular executable (double-click)
to get the full debug outpu because there seem to be issues with the MinGW output.
The Windows Terminal can be opened in Eclipse by right clicking on the `_bin` folder in the project explorer and clicking
Show in Local Terminal

## Setting up Eclipse - Makefile

The separate [Eclipse README](README-eclipse#top) specifies how to set up Eclipse. Separate project files and launch
configurations for the MinGW build were provided.






################################################################################
# CMake support for the Flight Software Framework
# 
# Developed in an effort to replace Make with a modern build system.
# 
# Author: R. Mueller
################################################################################

################################################################################
# Pre-Project preparation
################################################################################
cmake_minimum_required(VERSION 3.13)

# set(CMAKE_VERBOSE TRUE)
# set(RTEMS_VERBOSE TRUE)

set(CMAKE_SCRIPT_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

if(NOT OS_FSFW)
    set(OS_FSFW host CACHE STRING "OS for the FSFW.")
endif()

if(TGT_BSP MATCHES "arm/raspberrypi" OR TGT_BSP MATCHES "arm/beagleboneblack")
    option(LINUX_CROSS_COMPILE OFF)
    set(FSFW_HAL_ADD_LINUX ON)
endif()

if(TGT_BSP MATCHES "arm/raspberrypi")
    set(FSFW_HAL_ADD_RASPBERRY_PI ON)
endif()

if(TGT_BSP MATCHES "arm/stm32h743zi-nucleo")
    set(FSFW_HAL_ADD_STM32H7 ON)
endif()

# Perform steps like loading toolchain files where applicable.
include(${CMAKE_SCRIPT_PATH}/PreProjectConfig.cmake)
pre_project_config()

# Project Name
project(fsfw_example ASM C CXX)


################################################################################
# Pre-Sources preparation
################################################################################

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Set names and variables
set(TARGET_NAME ${CMAKE_PROJECT_NAME}) 
set(LIB_FSFW_NAME fsfw)
set(LIB_FSFW_HAL_NAME fsfw_hal)

# Set path names
set(FSFW_PATH fsfw)
set(MISSION_PATH mission)
set(COMMON_PATH common)
set(TEST_PATH test)
set(LWIP_PATH lwip)
set(LIB_FSFW_HAL_PATH fsfw_hal)

# Analyse different OS and architecture/target options, determine BSP_PATH,
# display information about compiler etc.
include (${CMAKE_SCRIPT_PATH}/HardwareOsPreConfig.cmake)
pre_source_hw_os_config()

set(COMMON_CONFIG_PATH "${COMMON_PATH}/config")
set(FSFW_CONFIG_PATH "${BSP_PATH}/fsfwconfig")
set(FSFW_ADDITIONAL_INC_PATHS 
    "${COMMON_CONFIG_PATH}"
    "${CMAKE_CURRENT_BINARY_DIR}"
    CACHE STRING
    "FSFW configuration paths"
)

configure_file(${COMMON_CONFIG_PATH}/commonConfig.h.in commonConfig.h)
configure_file(${FSFW_CONFIG_PATH}/FSFWConfig.h.in FSFWConfig.h)
configure_file(${FSFW_CONFIG_PATH}/OBSWConfig.h.in OBSWConfig.h)

if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    set(WARNING_FLAGS
        -Wall
        -Wextra
        -Wimplicit-fallthrough=1
        -Wno-unused-parameter
        -Wno-psabi
    )

    set(SHADOW_LOCAL_WARNING ON)
    if(TGT_BSP MATCHES "arm/raspberrypi" OR TGT_BSP MATCHES "arm/beagleboneblack")
        set(SHADOW_LOCAL_WARNING OFF)
    endif()

    if(SHADOW_LOCAL_WARNING)
        # Some older compilers emit odd warnings if this is used.
        set(WARNING_FLAGS ${WARNING_FLAGS} -Wshadow=local)
    endif()

    set(FSFW_WARNING_FLAGS ${WARNING_FLAGS})
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    add_compile_options(/permissive- /d2SSAOptimizer-)
    # To avoid nameclashes with min and max macro
    add_compile_definitions(NOMINMAX)
endif()

################################################################################
# Executable and Sources
################################################################################

# Add executable
add_executable(${TARGET_NAME})

# Add subdirectories
if(LIB_OS_NAME)
    add_subdirectory(${LIB_OS_NAME})
endif()
if(ADD_LWIP_STACK)
    add_subdirectory(${LWIP_PATH})
endif()
add_subdirectory(${BSP_PATH})
add_subdirectory(${FSFW_PATH})
add_subdirectory(${MISSION_PATH})
add_subdirectory(${COMMON_PATH})
add_subdirectory(${TEST_PATH})
add_subdirectory(${LIB_FSFW_HAL_PATH})

################################################################################
# Post-Sources preparation
################################################################################

# Add libraries for all sources.
target_link_libraries(${TARGET_NAME} PRIVATE
    ${LIB_FSFW_NAME} 
    ${LIB_OS_NAME} 
    ${LIB_FSFW_HAL_NAME}
)

# Add include paths for all sources.
target_include_directories(${TARGET_NAME} PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_BINARY_DIR}
    ${FSFW_CONFIG_PATH}
)    


if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    target_link_options(${TARGET_NAME} PRIVATE
        "-Wl,-Map=${TARGET_NAME}.map"
    )

    # Remove unused sections.
    target_compile_options(${TARGET_NAME} PRIVATE
        "-ffunction-sections"
        "-fdata-sections"
    )

    # Removed unused sections.
    if(NOT ${OS_FSFW} MATCHES rtems)
        target_link_options(${TARGET_NAME} PRIVATE
            "-Wl,--gc-sections"
        )
    endif()

    if(TGT_BSP MATCHES "arm/stm32h743zi-nucleo")
        target_link_options(${TARGET_NAME} PRIVATE
            -Wl,--undefined,_printf_float -Wl,--undefined,_scanf_float
        )
    endif()
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
endif()

if(CMAKE_VERBOSE)
    message(STATUS "Warning flags: ${WARNING_FLAGS}")
endif()
         

# Compile options for all sources.
target_compile_options(${TARGET_NAME} PRIVATE
    ${WARNING_FLAGS}
)

if(CMAKE_CROSSCOMPILING)
    include(${CMAKE_SCRIPT_PATH}/HardwareOsPostConfig.cmake)
    post_source_hw_os_config()
endif()

if(NOT CMAKE_SIZE)
    set(CMAKE_SIZE size)
    if(WIN32)
        set(FILE_SUFFIX ".exe")
    endif()
endif()

if(TGT_BSP)
    set(TARGET_STRING "Target BSP: ${TGT_BSP}")
else()
    set(TARGET_STRING "Target BSP: Hosted")
endif()

string(CONCAT POST_BUILD_COMMENT
    "Build directory: ${CMAKE_BINARY_DIR}\n"
    "Target OSAL: ${OS_FSFW}\n"
    "Target Build Type: ${CMAKE_BUILD_TYPE}\n"
    "${TARGET_STRING}"
)

add_custom_command(
   TARGET ${TARGET_NAME}
   POST_BUILD
   COMMAND ${CMAKE_SIZE} ${TARGET_NAME}${FILE_SUFFIX}
   COMMENT ${POST_BUILD_COMMENT}
)

include (${CMAKE_SCRIPT_PATH}/BuildType.cmake)
set_build_type()






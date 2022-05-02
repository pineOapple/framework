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

set(CMAKE_SCRIPT_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

if(NOT FSFW_OSAL)
  set(FSFW_OSAL host CACHE STRING "OS for the FSFW.")
endif()

# Project Name
project(fsfw-example-hosted C CXX)

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
set(COMMON_PATH example_common)
set(LIB_FSFW_HAL_PATH fsfw_hal)

set(BSP_PATH "bsp_hosted")
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

set(FSFW_ADD_MONITORING ON)

if(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  set(WARNING_FLAGS
    -Wall
    -Wextra
    -Wimplicit-fallthrough=1
    -Wno-unused-parameter
    -Wno-psabi
    )

  set(FSFW_WARNING_FLAGS ${WARNING_FLAGS})
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  add_compile_options(/permissive- /d2SSAOptimizer-)
  # To avoid nameclashes with min and max macro
  add_compile_definitions(NOMINMAX)
endif()

if(FSFW_OSAL MATCHES linux)
  find_package(Threads REQUIRED)
  # Hosted
else()

  if(WIN32)
  elseif(UNIX)
    find_package(Threads REQUIRED)
  endif()
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
add_subdirectory(${BSP_PATH})
add_subdirectory(${FSFW_PATH})
add_subdirectory(${COMMON_PATH})

################################################################################
# Post-Sources preparation
################################################################################

# Add libraries for all sources.
target_link_libraries(${TARGET_NAME} PRIVATE
  ${LIB_FSFW_NAME}
  ${LIB_OS_NAME}
  # ${LIB_FSFW_HAL_NAME}
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
  target_link_options(${TARGET_NAME} PRIVATE
    "-Wl,--gc-sections"
    )
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
endif()

if(CMAKE_VERBOSE)
  message(STATUS "Warning flags: ${WARNING_FLAGS}")
endif()


# Compile options for all sources.
target_compile_options(${TARGET_NAME} PRIVATE
  ${WARNING_FLAGS}
  )

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
  "Target OSAL: ${FSFW_OSAL}\n"
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

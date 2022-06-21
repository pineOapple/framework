target_sources(${TARGET_NAME} PRIVATE main.cpp)

add_subdirectory(core)
add_subdirectory(fsfwconfig)
add_subdirectory(utility)

target_include_directories(${TARGET_NAME} PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})

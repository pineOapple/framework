function(post_source_hw_os_config)

set(C_FLAGS "" CACHE INTERNAL "C flags")

set(C_DEFS "" CACHE INTERNAL "C Defines")

set(CXX_FLAGS ${C_FLAGS})
set(CXX_DEFS ${C_DEFS})

if(CMAKE_VERBOSE)
	message(STATUS "C Flags: ${C_FLAGS}")
	message(STATUS "CXX Flags: ${CXX_FLAGS}")
	message(STATUS "C Defs: ${C_DEFS}")
	message(STATUS "CXX Defs: ${CXX_DEFS}")
endif()

# Generator expression. Can be used to set different C, CXX and ASM flags.
target_compile_options(${TARGET_NAME} PRIVATE
	$<$<COMPILE_LANGUAGE:C>:${C_DEFS} ${C_FLAGS}>
	$<$<COMPILE_LANGUAGE:CXX>:${CXX_DEFS} ${CXX_FLAGS}>
	$<$<COMPILE_LANGUAGE:ASM>:${ASM_FLAGS}>
)

endfunction()
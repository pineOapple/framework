function(pre_source_hw_os_config)

if(${OS_FSFW} STREQUAL linux)
	find_package(Threads REQUIRED)
# Hosted
else()
	set(BSP_PATH "bsp_hosted")
	if(WIN32)
	elseif(UNIX)
		find_package(Threads REQUIRED)
	endif()
endif()
		
set(BSP_PATH ${BSP_PATH} PARENT_SCOPE)

endfunction()

function(pre_source_hw_os_config)

# FreeRTOS
if(${OS_FSFW} MATCHES freertos)
	add_definitions(-DFREERTOS)
# RTEMS
elseif(${OS_FSFW} STREQUAL rtems)
	add_definitions(-DRTEMS)
elseif(${OS_FSFW} STREQUAL linux)
	add_definitions(-DUNIX -DLINUX)	
	find_package(Threads REQUIRED)
	set(BSP_PATH "bsp_linux")
# Hosted
else()
	set(BSP_PATH "bsp_hosted")
	if(WIN32)
    	add_definitions(-DWIN32)
	elseif(UNIX)
		find_package(Threads REQUIRED)
		add_definitions(-DUNIX -DLINUX)	
	endif()
endif()

# Cross-compile information
if(CMAKE_CROSSCOMPILING)
	# set(CMAKE_VERBOSE TRUE)

	message(STATUS "Cross-compiling for ${TGT_BSP} target")
	message(STATUS "Cross-compile gcc: ${CMAKE_C_COMPILER}")
	message(STATUS "Cross-compile g++: ${CMAKE_CXX_COMPILER}")
	
	if(CMAKE_VERBOSE)
		message(STATUS "Cross-compile linker: ${CMAKE_LINKER}")
		message(STATUS "Cross-compile size utility: ${CMAKE_SIZE}")
		message(STATUS "Cross-compile objcopy utility: ${CMAKE_OBJCOPY}")
		message(STATUS "Cross-compile ranlib utility: ${CMAKE_RANLIB}")
		message(STATUS "Cross-compile ar utility: ${CMAKE_AR}")
		message(STATUS "Cross-compile nm utility: ${CMAKE_NM}")
		message(STATUS "Cross-compile strip utility: ${CMAKE_STRIP}")
		message(STATUS 
			"Cross-compile assembler: ${CMAKE_ASM_COMPILER} "
			"-x assembler-with-cpp"
		)
		message(STATUS "ABI flags: ${ABI_FLAGS}")
		message(STATUS "Custom linker script: ${LINKER_SCRIPT}")
	endif()
	
	set_property(CACHE TGT_BSP 
		PROPERTY STRINGS  
		"arm/stm32h743zi-nucleo" "arm/raspberrypi"
	)
endif()
	
if(${TGT_BSP} MATCHES "arm/stm32h743zi-nucleo")
	add_definitions(-DSTM32H743ZI_NUCLEO)
	if(${OS_FSFW} MATCHES freertos)
        option(ADD_LWIP_STACK "Add LwIP stack for application" ON)
        
		set(LIB_OS_NAME "freertos" CACHE STRING "OS FSFW library name")
		set(BSP_PATH "bsp_stm32_freertos")
		set(BOARD_CONFIG_PATH 
			"${BSP_PATH}/STM32CubeH7/Boards/NUCLEO-H743ZI/Inc"
			CACHE STRING
			"Board configuration include path."
		)
		set(MIDDLEWARES_PATH
			"${BSP_PATH}/STM32CubeH7/Middlewares"
		)
		set(CMSIS_INC_PATH
			"${BSP_PATH}/STM32CubeH7/Drivers/CMSIS/Include"
			CACHE STRING
			"CMSIS include path"
		)
		set(FREERTOS_GENERIC_PORT_PATH 
			"${MIDDLEWARES_PATH}/Third_Party/FreeRTOS"
		)
		set(FREERTOS_PORT_PATH
			"${FREERTOS_GENERIC_PORT_PATH}/portable/GCC/ARM_CM7/r0p1"
		)
		set(FREERTOS_CONFIG_AND_PORT_PATHS
			"${FREERTOS_PORT_PATH}"
			"${BOARD_CONFIG_PATH}"
			"${CMSIS_INC_PATH}"
			CACHE STRING
			"FreeRTOS configuration and port paths."
		)
		
		set(FREERTOS_PORT_SOURCES 
			${FREERTOS_PORT_PATH}/port.c
			CACHE INTERNAL
			"FreeRTOS port sources"
		)
		set(LIB_STM_HAL_NAME "stm_hal" CACHE STRING "STM32 HAL library name")
		set(LIB_HAL_NAME ${LIB_STM_HAL_NAME} PARENT_SCOPE)
		set(LINK_HAL TRUE PARENT_SCOPE)
		
		set(STM_HAL_CONFIG_PATH
			"${BOARD_CONFIG_PATH}"
			CACHE INTERNAL
			"STM HAL config path."
		)
		
		set(STM_HAL_DEFINES 
			"USE_HAL_DRIVER"
			"STM32H743xx"
			CACHE INTERNAL
			"HAL defines for target machine"
		)
			
		set(LINKER_SCRIPT_PATH "${BSP_PATH}/STM32CubeH7/Boards/NUCLEO-H743ZI")
		set(LINKER_SCRIPT_NAME "STM32H743ZITx_FLASH.ld")
	
		get_filename_component(LINKER_SCRIPT 
			${LINKER_SCRIPT_PATH}/${LINKER_SCRIPT_NAME}
			REALPATH BASE_DIR ${CMAKE_SOURCE_DIR}
		)
	
		set(LINKER_SCRIPT ${LINKER_SCRIPT} CACHE STRING "Custom linker script")
		
		if(ADD_LWIP_STACK)
			set(LWIP_CONFIG_PATH
				"${BOARD_CONFIG_PATH}"
				CACHE INTERNAL
				"lwIP configuration include path"
			)
	
			set(LIB_LWIP_NAME "lwip" CACHE STRING "lwIP library name")
		endif()
		
	elseif(${OS_FSFW} MATCHES rtems)
        option(ADD_LWIP_STACK "Add LwIP stack for application" ON)
	
		set(BSP_PATH "bsp_stm32_rtems")
		set(BOARD_CONFIG_PATH "${BSP_PATH}/boardconfig")
		if(ADD_LWIP_STACK)
            set(LWIP_CONFIG_PATH
                "${BOARD_CONFIG_PATH}"
                CACHE INTERNAL
                "lwIP configuration include path"
            )
    
            set(LIB_LWIP_NAME "lwip" CACHE STRING "lwIP library name")
        endif()

	endif() # ${OS_FSFW} MATCHES XYZ
	
elseif(${TGT_BSP} MATCHES "arm/raspberrypi")
    add_definitions(-DRASPBERRY_PI)
elseif(${TGT_BSP} MATCHES "arm/beagleboneblack")
    add_definitions(-DBEAGLE_BONE_BLACK)
elseif(${TGT_BSP} MATCHES "host/none")
    option(ADD_LWIP_STACK "Add LwIP stack for application" OFF)

else() 
    option(ADD_LWIP_STACK "Add LwIP stack for application" OFF)

	if(TGT_BSP)
		message(WARNING "CMake not configured for this target!")
		message(FATAL_ERROR "Target: ${TGT_BSP}!")
	endif()
	
endif()
		
set(BSP_PATH ${BSP_PATH} PARENT_SCOPE)

endfunction()

function(pre_project_config)

# Basic input sanitization
if(DEFINED TGT_BSP)
	if(${TGT_BSP} MATCHES "arm/raspberrypi" AND NOT ${OS_FSFW} MATCHES linux)
		message(STATUS "FSFW OSAL invalid for specified target BSP ${TGT_BSP}!")
		message(STATUS "Setting valid OS_FSFW: linux") 
		set(OS_FSFW "linux")
		if(${TGT_BSP} MATCHES "arm/stm32h743zi-nucleo")
			if(NOT ${OS_FSFW} MATCHES freertos) 
				message(STATUS 
					"FSFW OSAL invalid for specified target BSP ${TGT_BSP}!"
				)
				message(STATUS "Setting valid OS_FSFW: freertos") 
				set(OS_FSFW "freertos")
			endif()
		endif()
	endif()
	
endif()

# Disable compiler checks for cross-compiling.
if(${OS_FSFW} MATCHES freertos)

	set(CMAKE_TOOLCHAIN_FILE 
		"${CMAKE_SCRIPT_PATH}/STM32FreeRTOSConfig.cmake"
		PARENT_SCOPE
	)

elseif(${OS_FSFW} MATCHES rtems)
	
	set(RTEMS_CONFIG_DIR 
		"${CMAKE_CURRENT_SOURCE_DIR}/cmake/rtems-cmake"
		CACHE FILEPATH
		"Directory containing the RTEMS *.cmake files"
	)
	
	include(${RTEMS_CONFIG_DIR}/RTEMSPreProjectConfig.cmake)
	
	if(NOT DEFINED RTEMS_PREFIX)
		if(NOT DEFINED ENV{RTEMS_PREFIX})
			message(FATAL_ERROR 
				"RTEMS_PREFIX must be set either manually or as an environment "
				"variable!"
			)
		else()
			message(STATUS 
				"Using environment variable RTEMS_PREFIX $ENV{RTEMS_PREFIX} "
			 	"as RTEMS prefix"
			 )
			set(RTEMS_PREFIX $ENV{RTEMS_PREFIX})
		endif()
	endif()
	
	if(${TGT_BSP} MATCHES "arm/stm32h743zi-nucleo")
		set(RTEMS_BSP "arm/nucleo-h743zi")
	else()
		if(NOT DEFINED RTEMS_BSP)
			if(NOT DEFINED ENV{RTEMS_BSP})
				message(FATAL_ERROR 
					"RTEMS_BSP must be set either manually or as an environment"
					"variable!"
				)
			else()
				set(RTEMS_BSP $ENV{RTEMS_BSP})
			endif()
		endif()
	endif()
	
	rtems_pre_project_config(${RTEMS_PREFIX} ${RTEMS_BSP})
	
	set(CMAKE_TOOLCHAIN_FILE 
		${RTEMS_CONFIG_DIR}/RTEMSToolchain.cmake 
		PARENT_SCOPE
	)
	
elseif(${OS_FSFW} STREQUAL linux AND TGT_BSP)
	if(${TGT_BSP} MATCHES "host/none")
	
	elseif(${TGT_BSP} MATCHES "arm/raspberrypi")
		if(NOT DEFINED ENV{RASPBIAN_ROOTFS})
			if(NOT RASPBIAN_ROOTFS)
				set(ENV{RASPBIAN_ROOTFS} "$ENV{HOME}/raspberrypi/rootfs")
			else()
				set(ENV{RASPBIAN_ROOTFS} "${RASPBIAN_ROOTFS}")
			endif()
		else()	
			message(STATUS 
				"RASPBIAN_ROOTFS from environmental variables used: "
				"$ENV{RASPBIAN_ROOTFS}"
			)
		endif()
	
		if(NOT DEFINED ENV{RASPBERRY_VERSION})
			if(NOT RASPBERRY_VERSION)
				message(STATUS "No RASPBERRY_VERSION specified, setting to 4")
				set(RASPBERRY_VERSION "4" CACHE STRING "Raspberry Pi version")
			else()
				message(STATUS 
					"Setting RASPBERRY_VERSION to ${RASPBERRY_VERSION}"
				)
				set(RASPBERRY_VERSION 
					${RASPBERRY_VERSION} CACHE STRING "Raspberry Pi version"
				)
			set(ENV{RASPBERRY_VERSION} ${RASPBERRY_VERSION})
			endif()
		else()
			message(STATUS 
				"RASPBERRY_VERSION from environmental variables used: "
				"$ENV{RASPBERRY_VERSION}"
			)
		endif()
        if(LINUX_CROSS_COMPILE)
            set(CMAKE_TOOLCHAIN_FILE
                "${CMAKE_SCRIPT_PATH}/RPiCrossCompileConfig.cmake"
                PARENT_SCOPE
            )
        endif()
    elseif(${TGT_BSP} MATCHES "arm/beagleboneblack")
        if(LINUX_CROSS_COMPILE)
            set(CMAKE_TOOLCHAIN_FILE
                "${CMAKE_SCRIPT_PATH}/BBBCrossCompileConfig.cmake"
                PARENT_SCOPE
            )
        endif()
	else()
		message(WARNING "Target BSP (TGT_BSP) ${TGT_BSP} unknown!")
	endif()
endif()

endfunction()

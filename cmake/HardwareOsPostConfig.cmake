function(post_source_hw_os_config)

if(${TGT_BSP} MATCHES "arm/stm32h743zi-nucleo")
	if(${OS_FSFW} MATCHES "freertos")

        if(ADD_LWIP_STACK)
            message(STATUS "Linking against ${LIB_LWIP_NAME} lwIP library")
			if(LIB_LWIP_NAME)
				target_link_libraries(${TARGET_NAME} PUBLIC 
					${LIB_LWIP_NAME}
				)
			else()
				message(WARNING "lwIP library name not set!")
			endif()
        endif()

        if(LINK_HAL)
            message(STATUS "Linking against ${LIB_HAL_NAME} HAL library")
            if(LIB_HAL_NAME)
                target_link_libraries(${TARGET_NAME} PUBLIC
						${LIB_HAL_NAME}
				)
			else()
                message(WARNING "HAL library name not set!")
			endif()
		endif()
		
	elseif(${OS_FSFW} MATCHES "rtems")
	
        if(ADD_LWIP_STACK)
            message(STATUS "Linking against ${LIB_LWIP_NAME} lwIP library")
            if(LIB_LWIP_NAME)
                target_link_libraries(${TARGET_NAME} PUBLIC 
                    ${LIB_LWIP_NAME}
                )
            else()
                message(WARNING "lwIP library name not set!")
            endif()
        endif()
		
		include("${RTEMS_CONFIG_DIR}/RTEMSPostProjectConfig.cmake")
		rtems_post_project_config(${TARGET_NAME})
		
	endif()
endif()

if(LINKER_SCRIPT)
	target_link_options(${TARGET_NAME} PRIVATE
		-T${LINKER_SCRIPT}
	)
endif()
	
set(C_FLAGS "" CACHE INTERNAL "C flags")

set(C_DEFS ""
	CACHE INTERNAL
	"C Defines"
)

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

add_custom_command(
	TARGET ${TARGET_NAME}
	POST_BUILD
	COMMAND echo Generating binary file ${CMAKE_PROJECT_NAME}.bin..
	COMMAND ${CMAKE_OBJCOPY} -O binary ${TARGET_NAME} ${TARGET_NAME}.bin
)

endfunction()
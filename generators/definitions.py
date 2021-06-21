import enum

DATABASE_NAME = "fsfw_mod.db"


class BspSelect(enum.Enum):
    BSP_HOSTED = enum.auto()
    BSP_LINUX = enum.auto()
    BSP_STM32_FREERTOS = enum.auto()
    BSP_STM32_RTEMS = enum.auto()


BspFolderDict = {
    BspSelect.BSP_HOSTED.value: "bsp_hosted",
    BspSelect.BSP_LINUX.value: "bsp_linux",
    BspSelect.BSP_STM32_FREERTOS.value: "bsp_stm32_freertos",
    BspSelect.BSP_STM32_RTEMS.value: "bsp_stm32_rtems",
}

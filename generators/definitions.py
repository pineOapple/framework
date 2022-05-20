import os
import enum
from pathlib import Path


def determine_obsw_root_path() -> str:
    for _ in range(5):
        if os.path.exists("CMakeLists.txt"):
            return os.path.abspath(os.curdir)
        else:
            os.chdir("..")


PATH_VAR_ROOT = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = PATH_VAR_ROOT
OBSW_ROOT_DIR = Path(determine_obsw_root_path())
COMMON_SUBMODULE_NAME = "example_common"
EXAMPLE_COMMON_DIR = f"{OBSW_ROOT_DIR}/{COMMON_SUBMODULE_NAME}"
DATABASE_NAME = "eive_mod.db"
BSP_HOSTED = "bsp_hosted"

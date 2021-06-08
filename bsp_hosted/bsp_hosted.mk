CSRC += $(wildcard $(CURRENTPATH)/*.c)
CXXSRC += $(wildcard $(CURRENTPATH)/*.cpp)

CSRC += $(wildcard $(CURRENTPATH)/core/*.c)
CXXSRC += $(wildcard $(CURRENTPATH)/core/*.cpp)

CSRC += $(wildcard $(CURRENTPATH)/utility/*.c)

INCLUDES += $(CURRENTPATH)
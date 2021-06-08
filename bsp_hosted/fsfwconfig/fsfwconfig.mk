CXXSRC += $(wildcard $(CURRENTPATH)/datapool/*.cpp)
CXXSRC += $(wildcard $(CURRENTPATH)/events/*.cpp)
CXXSRC += $(wildcard $(CURRENTPATH)/ipc/*.cpp)
CXXSRC += $(wildcard $(CURRENTPATH)/objects/*.cpp)
CXXSRC += $(wildcard $(CURRENTPATH)/pollingsequence/*.cpp)

INCLUDES += $(CURRENTPATH)
INCLUDES += $(CURRENTPATH)/events
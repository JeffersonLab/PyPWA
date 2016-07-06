cmake_minimum_required(VERSION 3.5)
project(micAMP)

enable_language(C Fortran)

file(GLOB AMP_DATA_FILES "data/*.dat")

file(COPY ${AMP_DATA_FILES} DESTINATION "data")
file(COPY "fitterMIC.py" DESTINATION "fitterMIC.py")

set(CMAKE_CXX_COMPILER "icpc")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")


set(SOURCE_LIB1 micAmp.cpp)

set(SOURCE_LIB2 AMP.F)

add_library(micAMP SHARED ${SOURCE_LIB1})
add_library(AMP SHARED ${SOURCE_LIB2})

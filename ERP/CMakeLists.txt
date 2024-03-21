cmake_minimum_required(VERSION 3.10)

project(ERP)

include_directories(include)

file(GLOB PROJECT_SOURCES src/*.cpp)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_executable(ERP ${PROJECT_SOURCES})
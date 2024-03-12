cmake_minimum_required(VERSION 3.10)

project(MES)

include_directories(include)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_executable(MES src/main.cpp)
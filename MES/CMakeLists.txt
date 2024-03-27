cmake_minimum_required(VERSION 3.10)

project(MES)

set(CMAKE_PREFIX_PATH "C:/open62541-1.3/build")

find_package(open62541 REQUIRED)

include_directories(include)

file(GLOB PROJECT_SOURCES src/*.cpp src/*.c)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_executable(MES ${PROJECT_SOURCES})

target_link_libraries(MES PRIVATE open62541::open62541)

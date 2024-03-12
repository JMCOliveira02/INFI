cmake_minimum_required(VERSION 3.10)

project(ERP)

include_directories(include)

set(PROJECT_SOURCES
        src/main.cpp
        src/tiniXML2.cpp
        src/UDP_comms.cpp 
        src/XML_utils.cpp
)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_executable(ERP ${PROJECT_SOURCES})
cmake_minimum_required(VERSION 3.15)
project(render_ellipse LANGUAGES CXX)

set(CMAKE_POSITION_INDEPENDENT_CODE ON)

add_subdirectory(extern/pybind11)
add_subdirectory(cpp)

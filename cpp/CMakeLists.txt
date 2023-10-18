set(CMAKE_BUILD_TYPE Debug)
add_library(convex_polygon src/convex_polygon.cpp src/pixel_ellipse.cpp)
target_include_directories(convex_polygon PUBLIC ${PROJECT_SOURCE_DIR}/extern/spdlog/include)
set_property(TARGET convex_polygon PROPERTY CXX_STANDARD 14)

pybind11_add_module(ascii_shapes bindings/pybind_module.cpp)
target_include_directories(ascii_shapes PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${PROJECT_SOURCE_DIR}/extern/spdlog/include)
target_link_libraries(ascii_shapes LINK_PUBLIC convex_polygon)

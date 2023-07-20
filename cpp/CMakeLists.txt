add_library(convex_polygon src/convex_polygon.cpp src/pixel_ellipse.cpp)
set_property(TARGET convex_polygon PROPERTY CXX_STANDARD 14)

pybind11_add_module(ascii_shapes bindings/pybind_module.cpp)
target_include_directories(ascii_shapes PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
target_link_libraries(ascii_shapes LINK_PUBLIC convex_polygon)

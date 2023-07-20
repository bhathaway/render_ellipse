#include <pybind11/pybind11.h>
#include <sstream>

#include "src/convex_polygon.h"


namespace py = pybind11;

// Note: The module name _must_ match what's in the CMakeLists.txt
PYBIND11_MODULE(ascii_shapes, m) {
  m.doc() = "ascii_shapes python plugin";

  py::class_<Vector2d>(m, "Vector2d")
    .def(py::init<double, double>())
    .def("normal", &Vector2d::normal)
    .def("dot", &Vector2d::dot)
    .def("scaled_by", &Vector2d::scaled_by)
    .def("x", &Vector2d::x)
    .def("y", &Vector2d::y)
    .def("__repr__", &Vector2d::to_string);
}

#include <pybind11/pybind11.h>
#include <sstream>

#include "src/convex_polygon.h"


namespace py = pybind11;

// Note: The module name _must_ match what's in the CMakeLists.txt
PYBIND11_MODULE(ascii_shapes, m) {
  m.doc() = "ascii_shapes python plugin";

  auto m_convex_polygon = m.def_submodule("convex_polygon");

  py::class_<Vector2d>(m_convex_polygon, "Vector2d")
    .def(py::init<double, double>())
    .def("normal", &Vector2d::normal)
    .def("dot", &Vector2d::dot)
    .def("scaled_by", &Vector2d::scaled_by)
    .def_property("x", &Vector2d::x, nullptr)
    .def_property("y", &Vector2d::y, nullptr)
    .def("__repr__", &Vector2d::to_string);
}

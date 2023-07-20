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
    .def(py::init([](py::tuple t) {
      return Vector2d(t[0].cast<double>(), t[1].cast<double>());
    }))
    .def("normal", &Vector2d::normal)
    .def("dot", &Vector2d::dot)
    .def("scaled_by", &Vector2d::scaled_by)
    .def_property("x", &Vector2d::x, nullptr)
    .def_property("y", &Vector2d::y, nullptr)
    .def("__eq__", &Vector2d::operator==)
    .def("__repr__", &Vector2d::to_string);

  py::implicitly_convertible<py::tuple, Vector2d>();

  py::class_<Point2d>(m_convex_polygon, "Point2d")
    .def(py::init<double, double>())
    .def(py::init([](py::tuple t) {
      return Point2d(t[0].cast<double>(), t[1].cast<double>());
    }))
    .def("minus", &Point2d::minus)
    .def("plus", &Point2d::plus)
    .def_property("x", &Point2d::x, nullptr)
    .def_property("y", &Point2d::y, nullptr)
    .def("__eq__", &Point2d::operator==)
    .def("__repr__", &Point2d::to_string);

  py::implicitly_convertible<py::tuple, Point2d>();

  py::class_<HalfSpace>(m_convex_polygon, "HalfSpace")
    .def(py::init<const Point2d&, const Point2d&>())
    .def("contains", &HalfSpace::contains)
    .def("intersection", &HalfSpace::intersection)
    .def("__repr__", &HalfSpace::to_string);
}

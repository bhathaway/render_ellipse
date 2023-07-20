#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <sstream>

#include "src/convex_polygon.h"
#include "src/pixel_ellipse.h"

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
    .def("__eq__", &Vector2d::operator==)
    .def("__repr__", &Vector2d::to_string);

  py::class_<Point2d>(m_convex_polygon, "Point2d")
    .def(py::init<double, double>())
    .def("minus", &Point2d::minus)
    .def("plus", &Point2d::plus)
    .def_property("x", &Point2d::x, nullptr)
    .def_property("y", &Point2d::y, nullptr)
    .def("__eq__", &Point2d::operator==)
    .def("__repr__", &Point2d::to_string);

  py::class_<HalfSpace>(m_convex_polygon, "HalfSpace")
    .def(py::init<const Point2d&, const Point2d&>())
    .def("contains", &HalfSpace::contains)
    .def("intersection", &HalfSpace::intersection)
    .def("__repr__", &HalfSpace::to_string);

  py::class_<ConvexPolygon>(m_convex_polygon, "ConvexPolygon")
    .def(py::init<const std::vector<Point2d>&>())
    .def("edge_count", &ConvexPolygon::edge_count)
    .def("get_vertex", &ConvexPolygon::get_vertex)
    .def("area", &ConvexPolygon::area)
    .def("trim", &ConvexPolygon::trim)
    .def("contains", &ConvexPolygon::contains);

  auto m_pixel_ellipse = m.def_submodule("pixel_ellipse");

  py::class_<Pixel>(m_pixel_ellipse, "Pixel")
    .def(py::init<double, double>())
    .def("trim_outer", &Pixel::trim_outer,
         py::arg("p0"), py::arg("p1"), py::arg("reversed") = false)
    .def("trim_inner", &Pixel::trim_inner)
    .def_property("poly", &Pixel::poly, nullptr);
}

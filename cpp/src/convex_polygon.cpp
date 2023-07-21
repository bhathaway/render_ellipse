#include "convex_polygon.h"
#include <cassert>
#include <sstream>

Vector2d Vector2d::normal() const
{
  return Vector2d(-y_, x_);
}

double Vector2d::dot(const Vector2d& v) const
{
  return x_ * v.x_ + y_ * v.y_;
}

Vector2d Vector2d::scaled_by(double s) const
{
  return Vector2d(s * x_, s * y_);
}

bool Vector2d::operator==(const Vector2d& v) const
{
  return x_ == v.x_ && y_ == v.y_;
}

std::string Vector2d::to_string() const
{
  std::stringstream ss;
  ss << "v<" << x_ << ", " << y_ << '>';
  return ss.str();
}

Vector2d Point2d::minus(const Point2d& p) const
{
  return Vector2d(x_ - p.x_, y_ - p.y_);
}

Point2d Point2d::plus(const Vector2d& v) const
{
  return Point2d(x_ + v.x(), y_ + v.y());
}

bool Point2d::operator==(const Point2d& p) const
{
  return x_ == p.x_ && y_ == p.y_;
}

bool Point2d::operator<(const Point2d& p) const
{
  if (y_ < p.y_)
    return true;
  else if (y_ > p.y_)
    return false;
  else if (x_ < p.x_)
    return true;
  else
    return false;
}

std::string Point2d::to_string() const
{
  std::stringstream ss;
  ss << "p(" << x_ << ", " << y_ << ')';
  return ss.str();
}

HalfSpace::HalfSpace(const Point2d& p0, const Point2d& p1)
: point_(p0),
  normal_(p1.minus(p0).normal())
{ }

bool HalfSpace::contains(const Point2d& p) const
{
  const Vector2d test_v = p.minus(point_);
  return normal_.dot(test_v) >= 0;
}

Point2d HalfSpace::intersection(const Point2d& start, const Point2d& end) const
{
  Vector2d v0 = start.minus(point_);
  Vector2d v1 = end.minus(point_);
  const double q = v0.dot(normal_);
  const double r = v1.dot(normal_);
  // For now, I'm just going to make an assert:
  assert(q - r != 0.0);
  const double t = q / (q - r);
  const Vector2d v = end.minus(start);
  return start.plus(v.scaled_by(t));
}

std::string HalfSpace::to_string() const
{
  std::stringstream ss;
  ss << "hs{ " << point_.to_string() << ", " << normal_.to_string() << " }";
  return ss.str();
}

ConvexPolygon::ConvexPolygon(const std::vector<Point2d>& vertices)
: vertices_(vertices)
{
  assert(vertices.size() > 2);
  for (std::size_t i = 0; i < vertices.size(); ++i) {
    std::size_t next_i = i + 1;
    if (next_i == vertices.size())
      next_i = 0;
    halfspaces_.emplace_back(vertices[i], vertices[next_i]);
  }
}

std::size_t ConvexPolygon::edge_count() const
{
  return vertices_.size();
}

const Point2d& ConvexPolygon::get_vertex(std::size_t i) const
{
  return vertices_[i];
}

double ConvexPolygon::area() const
{
  double positive_diagonal_sum = 0;
  double negative_diagonal_sum = 0;
  for (std::size_t i = 0; i < vertices_.size(); ++i) {
    std::size_t k = i + 1;
    if (k == vertices_.size())
      k = 0;
    positive_diagonal_sum += vertices_[i].x() * vertices_[k].y();
    negative_diagonal_sum += vertices_[i].y() * vertices_[k].x();
  }

  return (positive_diagonal_sum - negative_diagonal_sum) / 2.0;
}

void ConvexPolygon::trim(const Point2d& start, const Point2d& end)
{
  const HalfSpace h(start, end);
  std::vector<Point2d> new_vertices;
  for (std::size_t i = 0; i < vertices_.size(); ++i) {
    const Point2d& current_point = vertices_[i];
    const Point2d& previous_point =
      i == 0 ? vertices_[vertices_.size() - 1] : vertices_[i - 1];

    if (h.contains(current_point)) {
      if (!h.contains(previous_point))
        new_vertices.push_back(h.intersection(previous_point, current_point));
      new_vertices.push_back(current_point);
    } else if (h.contains(previous_point)) {
      new_vertices.push_back(h.intersection(previous_point, current_point));
    }
  }

  vertices_ = new_vertices;
}

bool ConvexPolygon::contains(const Point2d& p) const
{
  for (const HalfSpace& h : halfspaces_)
    if (!h.contains(p))
      return false;

  return true;
}


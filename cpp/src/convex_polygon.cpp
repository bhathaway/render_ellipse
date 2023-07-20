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

std::string Point2d::to_string() const
{
  std::stringstream ss;
  ss << "p(" << x_ << ", " << y_ << ')';
  return ss.str();
}

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


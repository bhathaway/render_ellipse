#pragma once

#include <string>
#include <vector>

class Vector2d {
public:
  Vector2d(double x, double y)
  : x_(x), y_(y)
  { }

  Vector2d(const Vector2d&) = default;
  Vector2d& operator=(const Vector2d&) = default;

  Vector2d normal() const;
  double dot(const Vector2d&) const;
  Vector2d scaled_by(double) const;

  double x() const { return x_; }
  double y() const { return y_; }

  bool operator==(const Vector2d& v) const;

  std::string to_string() const;

private:
  double x_;
  double y_;
};

class Point2d {
public:
  Point2d(double x, double y)
  : x_(x), y_(y)
  { }

  Point2d(const Point2d&) = default;
  Point2d& operator=(const Point2d&) = default;

  Vector2d minus(const Point2d&) const;
  Point2d plus(const Vector2d&) const;

  double x() const { return x_; }
  double y() const { return y_; }

  bool operator==(const Point2d& p) const;

  std::string to_string() const;

private:
  double x_;
  double y_;
};

// Defines an "inside" with two points in counter-clockwise orientation
class HalfSpace {
public:
  HalfSpace(const Point2d& p0, const Point2d& p1);

  bool contains(const Point2d&) const;

  // Returns the intersection of the line containing p0 and p1 with the 
  // half space boundary
  Point2d intersection(const Point2d& p0, const Point2d& p1) const;

  std::string to_string() const;

private:
  Point2d point_;
  Vector2d normal_; // Points inside
};

class ConvexPolygon {
public:
  ConvexPolygon() = default;
  ConvexPolygon(const std::vector<Point2d>& vertices);

  std::size_t edge_count() const;
  const Point2d& get_vertex(std::size_t) const;
  double area() const;

  // Reduces a polgon by intersecting with the halfspace defined by [start, end>
  void trim(const Point2d& start, const Point2d& end);
  bool contains(const Point2d&) const;

private:
  std::vector<Point2d> vertices_;
  std::vector<HalfSpace> halfspaces_;
};

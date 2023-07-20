#pragma once

#include <string>

class Vector2d {
public:
  Vector2d(double x, double y)
  : x_(x), y_(y)
  { }

  Vector2d normal() const;
  double dot(const Vector2d&) const;
  Vector2d scaled_by(double) const;

  double x() const { return x_; }
  double y() const { return y_; }

  std::string to_string() const;

private:
  const double x_;
  const double y_;
};

class Point2d {
public:
  Point2d(double x, double y)
  : x_(x), y_(y)
  { }

  Vector2d minus(const Point2d&) const;
  Point2d plus(const Vector2d&) const;

  double x() const { return x_; }
  double y() const { return y_; }

  std::string to_string() const;

private:
  const double x_;
  const double y_;
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

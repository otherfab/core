// Exact geometric predicates
// Autogenerated by core/exact/simplicity: DO NOT EDIT
#pragma once

#include <other/core/vector/Vector.h>
namespace other {

// Is a 2D triangle positively oriented?
// Is a 2D triangle positively oriented?
bool triangle_oriented(const int p0i, const Vector<float,2> p0, const int p1i, const Vector<float,2> p1, const int p2i, const Vector<float,2> p2) OTHER_EXPORT;

// Is the rotation from a1-a0 to b1-b0 positive?
// Is the rotation from a1-a0 to b1-b0 positive?
bool segment_directions_oriented(const int a0i, const Vector<float,2> a0, const int a1i, const Vector<float,2> a1, const int b0i, const Vector<float,2> b0, const int b1i, const Vector<float,2> b1) OTHER_EXPORT;

// Given segments a,b,c, does intersect(a,b) come before intersect(a,c) on segment a?
// Given segments a,b,c, does intersect(a,b) come before intersect(a,c) on segment a?
// This predicate answers that question assuming that da,db and da,dc are positively oriented.
// This predicate answers that question assuming that da,db and da,dc are positively oriented.
bool segment_intersections_ordered_helper(const int a0i, const Vector<float,2> a0, const int a1i, const Vector<float,2> a1, const int b0i, const Vector<float,2> b0, const int b1i, const Vector<float,2> b1, const int c0i, const Vector<float,2> c0, const int c1i, const Vector<float,2> c1) OTHER_EXPORT;

}

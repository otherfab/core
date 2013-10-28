//#####################################################################
// Class Box
//#####################################################################
#include <othercore/geometry/Box.h>
#include <othercore/geometry/AnalyticImplicit.h>
#include <othercore/geometry/Ray.h>
#include <othercore/array/NdArray.h>
#include <othercore/array/Nested.h>
#include <othercore/array/view.h>
#include <othercore/python/from_python.h>
#include <othercore/python/exceptions.h>
#include <othercore/python/numpy.h>
#include <othercore/python/Ptr.h>
#include <othercore/python/wrap.h>
#include <othercore/math/cube.h>
#include <othercore/utility/format.h>
#include <othercore/structure/Tuple.h>
namespace other {

#ifdef OTHER_PYTHON

template<class T,int d> PyObject* to_python(const Box<Vector<T,d>>& box) {
  return to_python(new_<AnalyticImplicit<Box<Vector<T,d>>>>(box));
}

template<> PyObject* to_python(const Box<Vector<int,2>>& box) {
  return to_python(tuple(box.min,box.max));
}

template<> PyObject* to_python(const Box<Vector<int,3>>& box) {
  return to_python(tuple(box.min,box.max));
}

template<class T,int d> Box<Vector<T,d>> FromPython<Box<Vector<T,d>>>::convert(PyObject* object) {
  return from_python<AnalyticImplicit<Box<Vector<T,d>>>&>(object);
}

template<> Box<Vector<int,2>> FromPython<Box<Vector<int,2>>>::convert(PyObject* object) {
  Tuple<Vector<int,2>,Vector<int,2>> t = from_python<Tuple<Vector<int,2>,Vector<int,2>>>(object);
  return Box<Vector<int,2>>(t.x,t.y);
}

template<> Box<Vector<int,3>> FromPython<Box<Vector<int,3>>>::convert(PyObject* object) {
  Tuple<Vector<int,3>,Vector<int,3>> t = from_python<Tuple<Vector<int,3>,Vector<int,3>>>(object);
  return Box<Vector<int,3>>(t.x,t.y);
}

#endif

template<class T,int d> Vector<T,d> Box<Vector<T,d>>::surface(const TV& X) const {
  if (!lazy_inside(X)) return other::clamp(X,min,max);
  TV min_side = X-min,
     max_side = max-X,
     result = X;
  int min_argmin = min_side.argmin(),
      max_argmin = max_side.argmin();
  if (min_side[min_argmin]<=max_side[max_argmin])
    result[min_argmin] = min[min_argmin];
  else
    result[max_argmin] = max[max_argmin];
  return result;
}

template<class T,int d> T Box<Vector<T,d>>::phi(const TV& X) const {
  TV lengths = sizes();
  TV phi = abs(X-center())-(T).5*lengths;
  if (!all_less_equal(phi,TV()))
    return TV::componentwise_max(phi,TV()).magnitude();
  return phi.max();
}

template<class T,int d> Vector<T,d> Box<Vector<T,d>>::normal(const TV& X) const {
  if (lazy_inside(X)) {
    TV phis_max = X-max,
       phis_min = min-X;
    int axis = TV::componentwise_max(phis_min,phis_max).argmax();
    return T(phis_max[axis]>phis_min[axis]?1:-1)*TV::axis_vector(axis);
  } else {
    TV phis_max = X-max,
       phis_min = min-X;
    TV normal;
    for (int i=0;i<d;i++) {
      T phi = other::max(phis_min[i],phis_max[i]);
      normal[i] = phi>0?(phis_max[i]>phis_min[i]?phi:-phi):0;
    }
    return normal.normalized();
  }
}

template<class T,int d> string Box<Vector<T,d>>::name() {
  return format("Box<Vector<T,%d>",d);
}

template<class T,int d> string Box<Vector<T,d>>::repr() const {
  return format("Box(%s,%s)",tuple_repr(min),tuple_repr(max));
}

#define INSTANTIATION_HELPER(T,d) \
  template OTHER_CORE_EXPORT string Box<Vector<T,d>>::name(); \
  template OTHER_CORE_EXPORT string Box<Vector<T,d>>::repr() const; \
  template OTHER_CORE_EXPORT Vector<T,d> Box<Vector<T,d>>::normal(const Vector<T,d>&) const; \
  template OTHER_CORE_EXPORT Vector<T,d> Box<Vector<T,d>>::surface(const Vector<T,d>&) const; \
  template OTHER_CORE_EXPORT Vector<T,d>::Scalar Box<Vector<T,d>>::phi(const Vector<T,d>&) const; \
  OTHER_ONLY_PYTHON(template OTHER_CORE_EXPORT PyObject* to_python<T,d>(const Box<Vector<T,d>>&)); \
  OTHER_ONLY_PYTHON(template OTHER_CORE_EXPORT Box<Vector<T,d>> FromPython<Box<Vector<T,d>>>::convert(PyObject*));
INSTANTIATION_HELPER(int,2)
INSTANTIATION_HELPER(real,1)
INSTANTIATION_HELPER(real,2)
INSTANTIATION_HELPER(real,3)

#ifdef OTHER_PYTHON

static void bounding_box_py_helper(const int depth, Array<Box<real>>& box, PyObject* object) {
  if (const auto array = numpy_from_any(object,NumpyDescr<real>::descr(),0,100,NPY_ARRAY_CARRAY_RO,0)) {
    // object is a rectangular numpy array
    const int rank = PyArray_NDIM((PyArrayObject*)array);
    if (!rank) {
      OTHER_DECREF(array);
      throw TypeError("bounding_box: possibly nested array of vectors expected, found a bare scalar");
    }
    const int d = PyArray_DIMS((PyArrayObject*)array)[rank-1];
    if (!box.size())
      box.resize(d);
    if (box.size() != d) {
      OTHER_DECREF(array);
      throw TypeError(format("bounding_box: vectors of different sizes found, including %d and %d",box.size(),d));
    }
    const int count = PyArray_SIZE((PyArrayObject*)array)/d;
    const real* data = (const real*)PyArray_DATA((PyArrayObject*)array);
    for (int i=0;i<count;i++)
      for (int j=0;j<d;j++)
        box[j].enlarge(data[i*d+j]);
    OTHER_DECREF(array);
  } else {
    if (depth > 20)
      throw RuntimeError("bounding_box: maximum recursion depth exceeded, maybe you passed in a str?");
    // object is either badly formed or has irregular dimensions.  Loop over the structure manually.
    const auto iterator = steal_ref_check(PyObject_GetIter(object));
    while (const auto item = steal_ptr(PyIter_Next(&*iterator)))
      bounding_box_py_helper(depth+1,box,item.get());
    if (PyErr_Occurred()) // PyIter_Next returns 0 for both done and error, so check what happened
      throw_python_error();
  }
}

static PyObject* bounding_box_py(PyObject* object) {
  if (is_numpy_array(object)) {
    const auto array = from_python<NdArray<const real>>(object);
    OTHER_ASSERT(array.rank()>=2);
    if (array.shape.back()==2)
      return to_python(bounding_box(vector_view<2>(array.flat)));
    else if (array.shape.back()==3)
      return to_python(bounding_box(vector_view<3>(array.flat)));
    else
      throw TypeError(format("bounding_box: 2D or 3D vectors expected, got %dD",array.shape.back()));
  } else if (is_nested_array(object))
    return bounding_box_py(&*nested_array_from_python_helper(object).y);

  // object is neither a numpy array nor a Nested, so loop over it manually
  Array<Box<real>> box;
  bounding_box_py_helper(0,box,object);
  if (box.size()==2)
    return to_python(Box<Vector<real,2>>(vec(box[0].min,box[1].min),           vec(box[0].max,box[1].max)));
  else if (box.size()==3)
    return to_python(Box<Vector<real,3>>(vec(box[0].min,box[1].min,box[2].min),vec(box[0].max,box[1].max,box[2].max)));
  else
    throw TypeError(format("bounding_box: 2D or 3D vectors expected, got %dD",box.size()));
}

#endif

}
using namespace other;

void wrap_box_vector() {
#ifdef OTHER_PYTHON
  OTHER_FUNCTION_2(bounding_box,bounding_box_py)
#endif
}

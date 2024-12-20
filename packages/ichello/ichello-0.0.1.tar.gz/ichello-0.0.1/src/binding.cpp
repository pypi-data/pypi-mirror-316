#include <nanobind/nanobind.h>
#include <nanobind/stl/string.h>
#include <nanobind/stl/vector.h>

#include "hello.hpp"

namespace nb = nanobind;
using namespace nb::literals;

NB_MODULE(ichello_ext, m) {
  m.def("say_hello", &hello::say_hello);

  m.def("get_sum", &hello::get_sum<double>);  
}

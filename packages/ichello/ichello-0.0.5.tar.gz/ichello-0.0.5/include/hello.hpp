#pragma once

#include <numeric>
#include <vector>
#include <string>
#include <iostream>

namespace hello{

void say_hello(const std::string& name)
{
  std::cout << "Hello " << name << std::endl;
}

template<typename T>
T get_sum(const std::vector<T>& input)
{
  return std::accumulate(input.begin(), input.end(), T{});
}

}

cmake_minimum_required(VERSION 3.18)

project(${SKBUILD_PROJECT_NAME} LANGUAGES CXX)

if (NOT SKBUILD)
  message(WARNING "This project should be launched through Scikit Build")
endif()

set(VERSION_INFO ${SKBUILD_PROJECT_VERSION})
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Python 3.8 REQUIRED COMPONENTS Interpreter Development.Module
  OPTIONAL_COMPONENTS Development.SABIModule)

find_package(nanobind CONFIG REQUIRED)

set(MODULE_NAME ${SKBUILD_PROJECT_NAME}_ext)

nanobind_add_module(${MODULE_NAME}
  STABLE_ABI # Target CPython Stable ABI for Python 3.12+
  NB_STATIC # Include nanobind in the binary
  src/binding.cpp)

target_include_directories(${MODULE_NAME} PRIVATE include)

install(TARGETS ${MODULE_NAME} LIBRARY DESTINATION ${SKBUILD_PROJECT_NAME})




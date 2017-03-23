cmake_minimum_required(VERSION 2.8)

include(conanbuildinfo.cmake)
conan_basic_setup()

set(CMAKE_PREFIX_PATH, "${CONAN_PROTOBUF_ROOT}")
add_subdirectory("protobuf-c-${CONAN_PACKAGE_VERSION}/build-cmake")

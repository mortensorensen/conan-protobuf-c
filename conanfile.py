from conans import ConanFile, CMake, tools
from conans.errors import ConanException
import os
import re


class ProtobufcConan(ConanFile):
    name = "protobuf-c"
    version = "1.2.1"
    license = "https://github.com/protobuf-c/protobuf-c/blob/master/LICENSE"
    url = "https://github.com/protobuf-c/protobuf-c"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    options = { "shared": [True, False] }
    default_options = "shared=False"
    description = "conan package for protobuf-c"
    requires = "Protobuf/[>2.0,<3.0]@kmaragon/stable"
    exports = "CMakeLists.txt"

    def config_options(self):
        if self.settings.compiler == 'gcc' and float(self.settings.compiler.version.value) >= 5.1:
            if self.settings.compiler.libcxx != 'libstdc++11':
                raise ConanException("You must use the setting compiler.libcxx=libstdc++11")

    def source(self):
        tools.download("https://github.com/protobuf-c/protobuf-c/archive/v1.2.1.zip",
                   "protobuf-c.zip")

        tools.unzip("protobuf-c.zip")
        os.unlink("protobuf-c.zip")

    def build(self):
        cmake = CMake(self.settings)
        finished_package = os.getcwd() + "/pkg"

        make_options = os.getenv("MAKEOPTS") or ""
        if not re.match("/[^A-z-a-z_-]-j", make_options):
            cpucount = tools.cpu_count()
            make_options += " -j %s" % (cpucount * 2)

        orig_cmakelists = "protobuf-c-%s/build-cmake/CMakeLists.txt" % self.version
        tools.replace_in_file(orig_cmakelists, "CMAKE_SOURCE_DIR", "CMAKE_CURRENT_SOURCE_DIR")
        tools.replace_in_file(orig_cmakelists, "CMAKE_BINARY_DIR", "CMAKE_CURRENT_BINARY_DIR")

        libtype = "SHARED" if self.options.shared else "STATIC"
        tools.replace_in_file(orig_cmakelists, 'ADD_LIBRARY(protobuf-c ${PC_SOURCES})', 'ADD_LIBRARY(protobuf-c %s ${PC_SOURCES})' % libtype)

        # cmake
        self.run('mkdir -p pkg && mkdir -p build')
        self.run('cd build && cmake %s -DCMAKE_SKIP_BUILD_RPATH=FALSE ' % cmake.command_line +
            '-DBUILD_SHARED_LIBS:BOOL=%s' % ("TRUE" if self.options.shared else "FALSE") +
            '-DCMAKE_BUILD_WITH_INSTALL_RPATH=TRUE -DCMAKE_INSTALL_RPATH="%s/lib" ' % finished_package +
            '-DCMAKE_INSTALL_PREFIX:PATH="%s" -DCMAKE_INSTALL_RPATH_USE_LINK_PATH=TRUE -f ../' % finished_package)

        # build
        self.run("cd build && make %s install" % make_options)
    def package(self):
        self.copy("*", dst="lib", src="pkg/lib")
        self.copy("*", dst="bin", src="pkg/bin")
        self.copy("*", dst="include", src="pkg/include")

    def package_info(self):
        if self.options.shared:
            self.cpp_info.libs = ["protobuf-c"]
        else:
            self.cpp_info.libs = ["libprotobuf-c.a"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.bindirs = ["bin"]

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class ProtobufcConan(ConanFile):
    name = "protobuf-c"
    version = "1.3.2"
    description = "A C implementation of the Google Protocol Buffers data serialization format"
    topics = ("conan", "protobuf", "protobuf-c", "messaging")
    url = "https://github.com/mortensorensen/conan-protobuf-c"
    homepage = "https://github.com/protobuf-c/protobuf-c"
    license = "https://github.com/protobuf-c/protobuf-c/blob/master/LICENSE"
    exports = ["LICENSE.md"]
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = {"shared": False}
    _source_subfolder = "source_subfolder"
    requires = "protobuf/3.9.1@bincrafters/stable"

    def source(self):
        source_url = "{0}/releases/download/v{2}/{1}-{2}.tar.gz".format(self.homepage, self.name, self.version)
        tools.get(source_url, sha256="53f251f14c597bdb087aecf0b63630f434d73f5a10fc1ac545073597535b9e74")
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        with tools.chdir(self._source_subfolder):
            args = ["--disable-protoc"]
            if self.options.shared:
                args.extend(["--disable-static", "--enable-shared"])
            else:
                args.extend(["--disable-shared", "--disable-static"])
            env_build = AutoToolsBuildEnvironment(self)
            env_build.configure(args=args)
            env_build.make(args=["V=0"])
            env_build.install()

    def package(self):
        self.copy(pattern="LICENSE", dst="licenses", src=self._source_subfolder)
        la = os.path.join(self.package_folder, "lib", "libprotobuf-c.dylib")
        if os.path.isfile(la):
            os.unlink(la)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

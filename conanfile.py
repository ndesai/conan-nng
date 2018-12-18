#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class NanomsgConan(ConanFile):
    name = "nanomsg"
    version = "1.1.2"
    description = "Simple high-performance implementation of several scalability protocols"
    topics = ("conan", "nanomsg", "communication", "messaging", "protocols")
    url = "https://github.com/bincrafters/conan-nanomsg"
    homepage = ""
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    short_paths = True
    options = {
       "shared": [True, False],
       "enable_doc": [True, False],
       "enable_getaddrinfo_a": [True, False],
       "enable_tests": [True, False],
       "enable_tools": [True, False],
       "enable_nanocat": [True, False],
    }

    default_options = {'shared': False, 'enable_doc': False, 'enable_getaddrinfo_a': True, 'enable_tests': False, 'enable_tools': True, 'enable_nanocat': True}

    _source_subfolder = "source_subfolder"

    def source(self):
        source_url = "https://github.com/nanomsg/nanomsg"
        tools.get("{0}/archive/{1}.tar.gz".format(source_url, self.version),sha256="3c52165a735c2fb597d2306593ae4b17900688b90113d4115ad8480288f28ccb")
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def build(self):
        cmake = CMake(self)
        cmake.definitions["NN_STATIC_LIB"] = not self.options.shared
        cmake.definitions["NN_ENABLE_DOC"] = self.options.enable_doc
        cmake.definitions["NN_ENABLE_GETADDRINFO_A"] = self.options.enable_getaddrinfo_a
        cmake.definitions["NN_TESTS"] = self.options.enable_tests
        cmake.definitions["NN_TOOLS"] = self.options.enable_tools
        cmake.definitions["NN_ENABLE_NANOCAT"] = self.options.enable_nanocat
        cmake.configure()
        cmake.build()
        cmake.install()

    def package(self):
        self.copy(pattern="LICENSE", dst="license", src=self._source_subfolder)
        self.copy("*.h", dst="include", src="install/include")
        self.copy("*.dll", dst="bin", src="install/bin")
        self.copy("*.lib", dst="lib", src="install/lib")
        self.copy("*.a", dst="lib", src="install/lib")
        self.copy("*.so*", dst="lib", src="install/lib")
        self.copy("*.dylib", dst="lib", src="install/lib")
        self.copy("nanocat*", dst="bin", src="install/bin")
        self.copy("*.*", dst="lib/pkgconfig", src="install/lib/pkgconfig")

    def package_info(self):
        self.cpp_info.libs = ["nanomsg"]

        if not self.options.shared:
            self.cpp_info.defines.extend(["NN_STATIC_LIB=ON"])

        if self.settings.os == "Windows":
            if not self.options.shared:
                self.cpp_info.libs.append('mswsock')
                self.cpp_info.libs.append('ws2_32')
        elif self.settings.os == "Linux":
            self.cpp_info.libs.append('anl')
            self.cpp_info.libs.append('pthread')

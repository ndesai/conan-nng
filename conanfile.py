#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools
import os


class NanomsgConan(ConanFile):
    name = "nng"
    version = "1.1.1"
    description = "Light-weight brokerless messaging"
    topics = ("conan", "nanomsg", "nng", "communication", "messaging", "protocols")
    url = "https://github.com/ndesai/conan-nng"
    homepage = "https://github.com/nanomsg/nng"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    short_paths = True
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "enable_tests": [True, False],
        "enable_tools": [True, False],
        "enable_nanocat": [True, False],
        "enable_coverage": [True, False],
        "enable_tls": [True, False]
    }
    default_options = {
        'shared': False,
        'fPIC': True,
        'enable_tests': False,
        'enable_tools': True,
        'enable_nanocat': True,
        'enable_coverage': True,
        'enable_tls': False,
        
    }
    _source_subfolder = "source_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        sha256 = "cec54ed40c8feb5c0c66f81cfd200e9b243639a75d1b6093c95ee55885273205"
        tools.get("{0}/archive/{1}.tar.gz".format(self.homepage, self.version), sha256=sha256)
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["BUILD_SHARED_LIBS"] = self.options.shared
        cmake.definitions["NNG_TESTS"] = self.options.enable_tests
        cmake.definitions["NNG_TOOLS"] = self.options.enable_tools
        cmake.definitions["NNG_ENABLE_NNGCAT"] = self.options.enable_nanocat
        cmake.definitions["NNG_ENABLE_COVERAGE"] = self.options.enable_coverage
        cmake.configure()
        return cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)

        # if not self.options.shared:
        #     self.cpp_info.defines.append("NN_STATIC_LIB=ON")

        if self.settings.os == "Windows" and not self.options.shared:
            self.cpp_info.libs.extend(['mswsock', 'ws2_32'])
        elif self.settings.os == "Linux":
            self.cpp_info.libs.extend(['anl', 'pthread'])

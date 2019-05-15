from conans import ConanFile, tools, errors, CMake
import os


class AppimageupdateConan(ConanFile):
    name = "appimageupdate"
    version = "continuous"
    license = "MIT"
    author = "Alexis Lopez Zubieta <contact@azubieta.net>"
    url = "https://github.com/appimage-conan-community/conan-AppImageUpdate"
    description = "AppImageUpdate lets you update AppImages in a decentral way using information embedded in the AppImage itself.   "
    topics = ("AppImage", "Update")
    settings = "os", "compiler", "build_type", "arch"
    requires = ("OpenSSL/1.1.1b@conan/stable"), ("zlib/1.2.11@conan/stable"), ("libcurl/7.64.1@bincrafters/stable"), \
               ("glib/2.40.0@appimage-conan-community/stable"), ("cairo/1.17.2@bincrafters/stable"), \
               ("qt/5.12.3@appimage-conan-community/stable"), ("libpng/1.6.36@bincrafters/stable")
    build_requires = ("cmake_installer/3.14.3@conan/stable")
    default_options = {"zlib:shared": True}
    generators = "cmake"
    exports_sources = "patches/*"

    def conanArchToSystem(self, conan_arch):
        if conan_arch == "x86":
            return "i386"
        if conan_arch == "x86_64":
            return "amd64"

        return conan_arch

    def configure(self):
        if self.settings.compiler.libcxx == "libstdc++":
            raise Exception("This package is only compatible with libstdc++11")

    def system_requirements(self):
        pkgs_name = None
        system_arch = self.conanArchToSystem(self.settings.arch)
        if tools.os_info.linux_distro == "ubuntu":
            pkgs_name = ["linux-libc-dev:%s" % system_arch, "libxext-dev:%s" % system_arch]

        if pkgs_name:
            installer = tools.SystemPackageTool()
            for pkg_name in pkgs_name:
                installer.install(pkg_name)

    def source(self):
        self.run("git clone https://github.com/AppImage/AppImageUpdate.git --branch=%s" % self.version)
        self.run("cd AppImageUpdate && git submodule update --init --recursive")
        tools.patch(base_path="AppImageUpdate", patch_file="patches/use_conan.patch")

    def build(self):
        cmake = CMake(self)
        cmake.definitions["USE_SYSTEM_GTEST"] = "OFF"
        cmake.definitions["CMAKE_USE_OPENSSL"] = "OFF"
        cmake.configure(source_folder="AppImageUpdate")
        cmake.build()

    def package(self):
        self.copy("libappimageupdate*.so", src="lib", dst="lib", keep_path=False)
        self.copy("libappimageupdate*.a", src="lib", dst="lib", keep_path=False)
        self.copy("*", src="bin", dst="bin", keep_path=False)
        self.copy("AppImageUpdate/include/appimage/update.h", dst="include/appimage", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))

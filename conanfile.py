from conans import ConanFile, tools, errors
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
    requires = ("zlib/1.2.11@conan/stable")
    default_options = {"zlib:shared": True}

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
            pkgs_name = ["linux-libc-dev:%s" % system_arch]

        if pkgs_name:
            installer = tools.SystemPackageTool()
            for pkg_name in pkgs_name:
                installer.install(pkg_name)

    def build(self):
        if (self.settings.build_type != "Release"):
            raise errors.ConanInvalidConfiguration("Only Release builds are supported.")

        if (self.settings.arch == "x86" or self.settings.arch == "x86_64"):
            # match the arch naming convention used in AppImageKit
            appimagetool_arch_name = "i386" if self.settings.arch == "x86" else self.settings.arch

            tools.download(
                "https://github.com/AppImage/AppImageUpdate/releases/download/%s/appimageupdatetool-%s.AppImage"
                % (self.version, appimagetool_arch_name), "appimageupdatetool-%s.AppImage" % appimagetool_arch_name)
        else:
            raise errors.ConanInvalidConfiguration("Unsuported arch: %s" % self.settings.arch)

        self.run("chmod +x appimageupdatetool-%s.AppImage && ./appimageupdatetool-%s.AppImage --appimage-extract"
                 % (appimagetool_arch_name, appimagetool_arch_name), run_environment=True)

        tools.download("https://raw.githubusercontent.com/AppImage/AppImageUpdate/continuous/include/appimage/update.h",
                       "update.h")

    def package(self):
        self.copy("*", dst="bin", src="squashfs-root/usr/bin")
        self.copy("*", dst="lib", src="squashfs-root/usr/lib")
        self.copy("update.h", dst="include/appimage")

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.env_info.PATH.append(os.path.join(self.package_folder, "bin"))

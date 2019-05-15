from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    command = "sudo apt-get -qq update && sudo apt-get -qq install -y linux-libc-dev libxext-dev desktop-file-utils"
    remotes = [("https://api.bintray.com/conan/appimage-conan-community/public-conan", "true", "appimage"),
               ("https://api.bintray.com/conan/bincrafters/public-conan", "true", "bincrafters")]
    builder = ConanMultiPackager(remotes=remotes, build_policy="missing", build_types=["Release"], archs=["x86_64"],
                                 docker_entry_script=command)
    builder.add_common_builds()
    for settings, options, env_vars, build_requires, reference in builder.items:
        settings["compiler.libcxx"] = "libstdc++11"
        settings["compiler.cppstd"] = "11"

    builder.run()

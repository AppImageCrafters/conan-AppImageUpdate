from cpt.packager import ConanMultiPackager

if __name__ == "__main__":
    remotes = [("https://api.bintray.com/conan/appimage-conan-community/public-conan", "true", "appimage"),
               ("https://api.bintray.com/conan/bincrafters/public-conan", "true", "bincrafters")]
    builder = ConanMultiPackager(remotes=remotes, build_policy="missing", build_types=["Release"])
    builder.add_common_builds()
    for settings, options, env_vars, build_requires, reference in builder.items:
        settings["compiler.libcxx"] = "libstdc++11"
        settings["cppstd"] = "11"

    builder.run()

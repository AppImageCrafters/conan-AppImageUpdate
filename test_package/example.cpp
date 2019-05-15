#include <iostream>
#include <appimage/update.h>

int main() {
    try {
        appimage::update::Updater updater("/no.AppImage");
    } catch (...) {
        // it's okay to ignore all we just want to test linking
    }
}

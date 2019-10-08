#include <iostream>
#include <QApplication>

#include <classifier/window.hpp>

int main(int argc, char **argv) {
    std::cout << "Hello, World!" << std::endl;
    QApplication app(argc, argv);
    Window window;
    window.show();
    return app.exec();
}

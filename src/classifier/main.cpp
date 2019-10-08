#include <QApplication>

#include <classifier/window.hpp>

int main(int argc, char **argv) {
    QApplication app(argc, argv);
    Window window;
    window.show();
    return app.exec();
}

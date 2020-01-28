#include <QApplication>
#include <QMainWindow>

#include <classifier/main_view.hpp>

int main(int argc, char **argv) {
    QApplication app(argc, argv);
    // Qt seems to take ownership of this object and frees it itself
    // accordingly, it needs to be dynamically allocated, but not deleted
    MainView *main_view = new MainView();

    QMainWindow window;
    window.setWindowTitle("Image Classifier");
    window.setCentralWidget(main_view);

    window.show();
    return app.exec();
}

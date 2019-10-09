#include <QApplication>
#include <QMainWindow>

#include <classifier/main_view.hpp>

int main(int argc, char **argv) {
    QApplication app(argc, argv);
    MainView *main_view = new MainView();

    QMainWindow window;
    window.setWindowTitle("Image Classifier");
    window.setCentralWidget(main_view);

    window.show();
    return app.exec();
}

#ifndef CLASSIFIER_WINDOW_H_
#define CLASSIFIER_WINDOW_H_

#include <QComboBox>
#include <QFormLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QLineEdit>
#include <QPixmap>
#include <QPushButton>
#include <QTextEdit>
#include <QVBoxLayout>
#include <QWidget>

#include <classifier/filepath_button.hpp>

class Window : public QWidget {
private:
    QVBoxLayout central_layout;

    // top of the window
    FilepathButton fpath_button;

    // organize the main window area
    QWidget content_widget;
    QHBoxLayout split_layout;

    // left side of the window
    QWidget form_section;
    QFormLayout form_layout;
    QComboBox letter_color_select;
    QComboBox letter_orientation_select;
    QLineEdit letter_entry;

    QWidget image_section;
    QVBoxLayout image_layout;
    QPixmap loaded_image;
    QLabel image_label;
    QTextEdit metadata_view;

public:
    explicit Window(QWidget *parent = nullptr);

};

#endif // CLASSIFIER_WINDOW_H_

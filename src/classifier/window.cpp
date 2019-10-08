#include <classifier/window.hpp>

Window::Window(QWidget *parent) {
    this->setLayout(&this->central_layout);
    this->central_layout.addWidget(&this->fpath_button);

    this->central_layout.addWidget(&this->content_widget);
    this->content_widget.setLayout(&this->split_layout);

    this->split_layout.addWidget(&this->form_widget);
    this->form_widget.setLayout(&this->form_layout);
    this->form_layout.addRow("Letter Color", &this->letter_color_select);
    this->form_layout.addRow("Letter Direction", &this->letter_orientation_select);
    this->form_layout.addRow("Letter", &this->letter_entry);

    this->letter_color_select.addItem("Orange");
    this->letter_color_select.addItem("Blue");
    this->letter_color_select.addItem("Red");
    this->letter_color_select.addItem("Green");

    this->letter_orientation_select.addItem("North");
    this->letter_orientation_select.addItem("South");
    this->letter_orientation_select.addItem("East");
    this->letter_orientation_select.addItem("West");
}

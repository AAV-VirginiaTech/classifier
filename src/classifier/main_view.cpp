#include <classifier/main_view.hpp>

MainView::MainView(QWidget *parent) {
    this->setLayout(&this->central_layout);
    this->central_layout.addWidget(&this->fpath_button);

    this->central_layout.addWidget(&this->content_widget);
    this->content_widget.setLayout(&this->split_layout);

    // everything below here is the left half of the window
    this->split_layout.addWidget(&this->form_section);
    this->form_section.setLayout(&this->form_layout);
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

    // everything below here is the right half of the window
    this->split_layout.addWidget(&this->image_section);
    this->image_section.setLayout(&this->image_layout);
    this->image_layout.addWidget(&this->image_label);
    this->image_layout.addWidget(&this->metadata_view);

    // load the stub image
    this->loaded_image.load("bluesquare.png");
    this->loaded_image = this->loaded_image.scaled(
        QSize(400, 400), Qt::AspectRatioMode::KeepAspectRatioByExpanding
    );
    this->image_label.setPixmap(loaded_image);
}

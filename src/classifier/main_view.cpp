#include <iostream>

#include <classifier/main_view.hpp>

MainView::MainView(QWidget *parent) :
    next_image_button("Next Image")
{
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
    this->image_layout.addWidget(&this->image_scroller);
    this->image_layout.addWidget(&this->next_image_button);
    this->image_layout.addWidget(&this->metadata_view);

    // place the image inside the scrollable area
    this->image_label.setSizePolicy(QSizePolicy::Ignored, QSizePolicy::Ignored);
    this->image_label.setScaledContents(true);
    this->image_scroller.setWidget(&this->image_label);

    // load the stub image
    this->newImageDirSelected(this->fpath_button.getCurrentPath());

    connect(&this->fpath_button, &FilepathButton::pathChanged, this, &MainView::newImageDirSelected);
    connect(&this->next_image_button, &QPushButton::pressed, this, &MainView::nextImageButtonPressed);
}

/**
 * This function reiterates the entire provided directory and displays
 * the first image that isn't in the displayed_images list. While
 * reiterating each time is computationally wasteful, it avoids the issue
 * of missing images that were added to the directory after the first
 * iteration.
 **/
void MainView::displayNextImage(const QString& dir_path) {
    QDir image_dir(dir_path);
    QStringList name_filters { "*.png", "*.jpg", "*.jpeg", "*.gif", "*.bmp" };
    image_dir.setNameFilters(name_filters);

    QStringList images = image_dir.entryList();
    for (const QString& image_fname : images) {
        if (!this->displayed_images.contains(image_fname)) {
            QString full_path = dir_path + "/" + image_fname;
            std::cerr << full_path.toStdString() << std::endl;

            this->loaded_image.load(full_path);
            auto viewport = this->image_scroller.viewport();
            QSize area(viewport->width(), viewport->height());
            this->loaded_image = this->loaded_image.scaled(
                area, Qt::AspectRatioMode::KeepAspectRatio
            );
            this->image_label.setPixmap(loaded_image);
            this->image_label.adjustSize();

            // track that we've displayed this image, stop searching for something to find
            this->displayed_images.append(image_fname);
            return;
        }
    }

    // if we've reached this point, then there are no new images
    // in the folder to display. This error message could be made
    // more aesthetically pleasing/user friendly.
    this->image_label.setText("No images to display");
}

void MainView::newImageDirSelected(QString dir_path) {
    this->displayed_images.clear();
    this->displayNextImage(dir_path);
}

void MainView::nextImageButtonPressed() {
    this->displayNextImage(this->fpath_button.getCurrentPath());
}

#include <QFileDialog>

#include <classifier/filepath_button.hpp>

FilepathButton::FilepathButton(QString initial_path) :
    fpath_label(initial_path),
    open_dialog_button("...")
{
    // the user can't edit the filepath field
    this->fpath_label.setEnabled(false);

    this->setLayout(&this->layout);
    this->open_dialog_button.setSizePolicy(QSizePolicy::Policy::Minimum, QSizePolicy::Policy::Fixed);
    this->layout.addWidget(&this->fpath_label);
    this->layout.addWidget(&this->open_dialog_button);

    this->dialog.setFileMode(QFileDialog::FileMode::DirectoryOnly);
    connect(&this->open_dialog_button, &QPushButton::pressed, this, &FilepathButton::buttonPressed);
    connect(&this->dialog, &QFileDialog::fileSelected, this, &FilepathButton::fileSelected);
}

QString FilepathButton::getCurrentPath() const {
    return this->fpath_label.text();
}

void FilepathButton::buttonPressed() {
    this->dialog.show();
}

void FilepathButton::fileSelected(const QString& fpath) {
    fpath_label.setText(fpath);
    emit this->pathChanged(fpath);
}

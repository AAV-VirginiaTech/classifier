#include <classifier/filepath_button.hpp>

FilepathButton::FilepathButton() :
    open_dialog_button("...")
{
    this->setLayout(&this->layout);
    this->open_dialog_button.setSizePolicy(QSizePolicy::Policy::Minimum, QSizePolicy::Policy::Fixed);
    this->layout.addWidget(&this->fpath_label);
    this->layout.addWidget(&this->open_dialog_button);
}

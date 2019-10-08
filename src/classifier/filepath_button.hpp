#ifndef CLASSIFIER_FPATH_BUTTON_H_
#define CLASSIFIER_FPATH_BUTTON_H_

#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QWidget>

class FilepathButton : public QWidget {
private:
    QHBoxLayout layout;
    QLabel fpath_label;
    QPushButton open_dialog_button;

public:
    explicit FilepathButton();
};

#endif // CLASSIFIER_FPATH_BUTTON_H_

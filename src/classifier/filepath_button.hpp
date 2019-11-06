#ifndef CLASSIFIER_FPATH_BUTTON_H_
#define CLASSIFIER_FPATH_BUTTON_H_

#include <QCoreApplication>
#include <QFileDialog>
#include <QHBoxLayout>
#include <QLineEdit>
#include <QPushButton>
#include <QWidget>

class FilepathButton : public QWidget {
    Q_OBJECT

private:
    QHBoxLayout layout;
    QLineEdit fpath_label;
    QPushButton open_dialog_button;

    QFileDialog dialog;

private slots:
    void buttonPressed();
    void fileSelected(const QString& fpath);

public:
    explicit FilepathButton(QString initial_path = QCoreApplication::applicationDirPath() + "/../example-images");

    QString getCurrentPath() const;

signals:
    void pathChanged(const QString& fpath);
};

#endif // CLASSIFIER_FPATH_BUTTON_H_

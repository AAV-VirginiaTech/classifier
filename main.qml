import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtQuick.Window 2.12
import QtQuick.Dialogs 1.2
import Qt.labs.folderlistmodel 2.12
import "style" as Style

Window {
    id: window
    visible: true
    width: 640
    height: 480
    title: qsTr("Image Classifier")

    FolderListModel {
        id: folderModel

        nameFilters: [ "*.png", "*.PNG", "*.jpg", "*.JPG" ]

        property int curIndex: 0
    }

    function displayImage(url) {
        imageView.source = url;
        imageRegion.zoomPercentage = 100;
    }

    Style.Style {
        id: style
    }

    Rectangle {
        id: topbar
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right

        height: style.toolbarHeight
        color: "#333333"

        Rectangle {
            id: filepathRegion
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            width: parent.width * 2 / 3

            color: "transparent"

            Text {
                id: filepathText
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left

                text: folderModel.folder
                color: "white"
            }
            Style.RoundButton {
                id: filepathButton
                anchors.verticalCenter: parent.verticalCenter
                anchors.right: parent.right

                text: "   Open   "

                onClicked: {
                    fileDialog.open()
                }
            }
            FileDialog {
                id: fileDialog
                title: "Please choose the image folder"
                folder: shortcuts.home
                selectMultiple: false
                selectFolder: true
                onAccepted: {
                    folderModel.folder = fileDialog.fileUrl;
                    folderModel.curIndex = 0;
                    if (folderModel.curIndex < folderModel.count) {
                        var image_path = folderModel.get(folderModel.curIndex, "fileURL");
                        window.displayImage(image_path);
                    }
                }
            }
        }
    }

    Rectangle {
        id: topbarSeparator
        anchors.top: topbar.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        height: 1 / Screen.devicePixelRatio

        color: "white"
    }

    Rectangle {
        id: formRegion
        anchors.top: topbarSeparator.bottom
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        width: 15 * style.em

        color: "#333333"

        ColumnLayout {
            id: formLayout
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.margins: this.spacing

            FormRow {
                Layout.fillWidth: true
                height: style.clickableHeight

                text: "Letter Color"
                model: ["Orange", "Blue", "Red", "Green"]
            }

            FormRow {
                Layout.fillWidth: true
                height: style.clickableHeight

                text: "Letter Direction"
                model: ["North", "South", "East", "West"]
            }

            FormRow {
                Layout.fillHeight: true
                height: style.clickableHeight

                text: "Letter"

                Style.RoundTextField {
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: parent.horizontalCenter
                    anchors.leftMargin: style.formCenterMargin
                    anchors.right: parent.right
                }
            }
        }
    }

    Rectangle {
        id: imageRegion
        anchors.top: topbarSeparator.bottom
        anchors.left: formRegion.right
        anchors.right: parent.right
        anchors.bottom: parent.bottom

        property real zoomPercentage: 100

        Flickable {
            id: scrollRegion
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: zoomToolbar.top

            // prevent the scaled image from going outside the bounds of this item
            clip: true

            Rectangle {
                id: imageContainer
                anchors.fill: parent

                color: "black"

                Image {
                    id: imageView
                    width: parent.width
                    height: parent.height

                    scale: imageRegion.zoomPercentage / 100

                    fillMode: Image.PreserveAspectFit

//                    source: "qrc:/example-images/triangle.png"
//                    source: folderModel.get(folderModel.curIndex, "fileURL")
                }

                MouseArea {
                    anchors.fill: parent

                    onWheel: {
                        imageRegion.zoomPercentage += wheel.angleDelta.y / 8;

                        // the image flips if we go negative, which is kinda weird for the user
                        // also, 0% zoom would be really bad
                        if (imageRegion.zoomPercentage < 20) {
                            imageRegion.zoomPercentage = 20;
                        }
                    }

                    drag.target: imageView
                    drag.axis: Drag.XAndYAxis

                    property real scaledWidth: imageView.width * imageRegion.zoomPercentage / 100;
                    property real scaledHeight: imageView.height * imageRegion.zoomPercentage / 100;
                    drag.minimumX: -scaledWidth + style.em
                    drag.maximumX: scaledWidth - style.em
                    drag.minimumY: -scaledHeight + style.em
                    drag.maximumY: scaledHeight - style.em
                }
            }
        }

        Rectangle {
            id: zoomToolbar
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            height: style.toolbarHeight

            color: "black"

            Style.RoundButton {
                id: nextImageButton

                anchors.left: parent.left
                anchors.verticalCenter: parent.verticalCenter
                anchors.margins: 5

                text: "Next Image"
                onClicked: {
                    folderModel.curIndex += 1;
                    window.displayImage(folderModel.get(folderModel.curIndex, "fileURL"));
                }
            }

            Text {
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter

                text: imageRegion.zoomPercentage + "%"
                color: "white"
            }

            Style.RoundButton {
                id: resetZoomButton

                anchors.right: parent.right
                anchors.verticalCenter: parent.verticalCenter
                anchors.margins: 5

                text: "Reset"
                onClicked: {
                    imageRegion.zoomPercentage = 100;
                }
            }
        }
    }
}

import QtQuick 2.12
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12
import QtQuick.Window 2.12
import QtQuick.Dialogs 1.2
import Qt.labs.folderlistmodel 2.12
import "style" as Style

Window {
    visible: true
    width: 640
    height: 480
    title: qsTr("Image Classifier")

    FolderListModel {
        id: folderModel
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
                    folderModel.folder = fileDialog.fileUrl
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
        property real translateX: 0
        property real translateY: 0

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
//                    anchors.fill: parent

                    scale: imageRegion.zoomPercentage / 100

                    fillMode: Image.PreserveAspectFit

                    source: "qrc:/example-images/triangle.png"
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
//                    drag.minimumX: 0
//                    drag.maximumX: imageContainer.width - imageView.width
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

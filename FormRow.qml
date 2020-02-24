import QtQuick 2.12
import "style" as Style

Item {
    id: root

    default property alias field: fieldContainer.field

    property string text: "Label"
    property color color: "white"
    property color background: "transparent"

    property var model: ["Default 1", "Default 2", "Default 3", "Default 4"]

    Style.Style {
        id: style
    }

    Rectangle {
        id: baseRect
        anchors.fill: parent
        color: root.background

        Text {
            id: label

            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left

            text: root.text
            color: root.color
        }
        Item {
            id: fieldContainer
            anchors.fill: parent

            property Item field: Style.RoundComboBox {
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.horizontalCenter
                anchors.leftMargin: style.formCenterMargin
                anchors.right: parent.right

                model: root.model
            }


            children: [field]
        }
    }
}

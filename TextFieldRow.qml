import QtQuick 2.0
import "style" as Style

Item {
    id: root

    property string text: "Label"
    property color color: "white"
    property color background: "transparent"

    property var validator: null
    property string inputMask: null
    property string startingText: ""

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
        Style.TextField {
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.horizontalCenter
            anchors.leftMargin: style.formCenterMargin
            anchors.right: parent.right

            text: root.startingText

            validator: root.validator
            inputMask: root.inputMask
        }
    }
}

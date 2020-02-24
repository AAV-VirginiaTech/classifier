import QtQuick 2.12
import QtQuick.Controls 2.12 as Controls

Controls.ComboBox {
    Style {
        id: style
    }

    height: style.clickableHeight

    background: Rectangle {
        anchors.fill: parent
        anchors.margins: 0
        radius: style.cornerRadius
    }
}

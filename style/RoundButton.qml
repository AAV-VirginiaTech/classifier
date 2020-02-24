import QtQuick 2.12
import QtQuick.Controls 2.12 as Controls

Controls.RoundButton {
    Style {
        id: style
    }

    height: style.clickableHeight
    radius: style.cornerRadius
    text: undefined
}

import QtQuick 2.12
import QtQuick.Window 2.12

QtObject {
    property var fontMetrics: FontMetrics {

    }

    property real em: fontMetrics.height
    property real clickableHeight: 2 * em
    property real formCenterMargin: 0.25 * em
    property real cornerRadius: 0.3 * clickableHeight
    property real toolbarHeight: 3 * em
}

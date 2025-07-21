import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Frame {
    height: 66
    RowLayout { anchors.fill: parent; spacing: 14; padding: 10
        Image { source: "images/group.png"; width: 37; height: 37 }
        Text { text: title; font.pixelSize: 16; font.styleName: "Semibold" }
        Item { Layout.fillWidth: true }
        Image { source: "images/tum.png"; width: 49; height: 23 }
    }
}
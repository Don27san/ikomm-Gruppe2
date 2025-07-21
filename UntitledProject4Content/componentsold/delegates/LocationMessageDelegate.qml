import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

RowLayout {
    spacing: 8;
    Rectangle {
        width: 250; height: 105; color: "#eeeeee"; radius: 16
        ColumnLayout { anchors.fill: parent; spacing: 8; padding: 12
            RowLayout { spacing: 8
                Rectangle { width: 40; height: 40; color: "#1f5cf1"; radius: 20
                    Image { source: "images/location_icon.png"; anchors.centerIn: parent; width: 15; height: 15 }
                }
                ColumnLayout { spacing: 4; width: 130
                    Text { text: qsTr("Live Location"); font.pixelSize: 14; font.weight: Font.DemiBold }
                    Text { text: message; font.pixelSize: 12; color: "#575757"; wrapMode: Text.WrapAnywhere }
                }
            }
            Button { text: qsTr("View Location"); Layout.fillWidth: true; height: 35; flat: true
                background: Rectangle { color: "#fafafa"; radius: 10 }
            }
        }
    }
}
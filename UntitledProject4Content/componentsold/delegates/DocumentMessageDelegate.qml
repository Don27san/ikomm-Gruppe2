import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle {
    property string content  // you can pack “name – size” or split into two props
    property bool outgoing: false

    width: 250; height: 105
    color: "#eeeeee"; radius: 16

    ColumnLayout {
        anchors.fill: parent; spacing: 8; Layout.margins: 12

        RowLayout { spacing: 8
            Rectangle {
                width: 40; height: 40; color: "#1f5cf1"; radius: 20
                Image {
                    source: "images/document_icon.png"
                    width: 15; anchors.centerIn: parent
                    fillMode: Image.PreserveAspectFit
                }
            }
            ColumnLayout { width: 130; spacing: 4
                Text {
                    text: content.split("||")[0] // name before separator
                    font.pixelSize: 14; font.weight: Font.DemiBold
                    width: 180; elide: Text.ElideRight
                }
                Text {
                    text: content.split("||")[1] // size after separator
                    font.pixelSize: 12; color: "#575757"
                    wrapMode: Text.WrapAnywhere; width: 175
                }
            }
        }

        Button {
            height: 35; flat: true
            contentItem: Rectangle {
                color: "#fafafa"; radius: 10; anchors.fill: parent
            }
            Text {
                text: qsTr("Download Document")
                font.pixelSize: 12; font.styleName: "Semibold"
                anchors.centerIn: parent
            }
            onClicked: documentRequested()
        }
    }

    signal documentRequested()
}

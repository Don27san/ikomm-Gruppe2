import QtQuick
import QtQuick.Controls

Rectangle {
    id: documentRoot
    
    property string fileName: "Document"
    property string fileSize: "0 KB"
    
    width: 250
    height: 105
    color: "#eeeeee"
    radius: 16
    
    Column {
        anchors.fill: parent
        spacing: 8
        padding: 12
        
        Row {
            spacing: 8
            
            Rectangle {
                width: 40
                height: 40
                color: "#1f5cf1"
                radius: 500

                Image {
                    width: 15
                    source: "../images/document_icon.png"
                    anchors.centerIn: parent
                    fillMode: Image.PreserveAspectFit
                }
            }

            Column {
                width: 130
                spacing: 4
                
                Text {
                    width: 180
                    text: fileName
                    elide: Text.ElideRight
                    font.pixelSize: 14
                    font.weight: Font.DemiBold
                }

                Text {
                    width: 175
                    color: "#575757"
                    text: fileSize
                    font.pixelSize: 12
                }
            }
        }

        Button {
            height: 35
            text: ""
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 12
            anchors.rightMargin: 12
            flat: true
            
            background: Rectangle {
                color: "#fafafa"
                radius: 10
            }

            Text {
                text: qsTr("Download Document")
                font.pixelSize: 12
                font.styleName: "Semibold"
                anchors.centerIn: parent
            }

            onClicked: {
                console.log("Download document:", fileName)
            }
        }
    }
}
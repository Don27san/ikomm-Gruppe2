import QtQuick
import QtQuick.Controls

Rectangle {
    id: typingRoot
    
    width: 60
    height: 36
    color: "#eeeeee"
    radius: 16
    
    AnimatedImage {
        width: 50
        source: "../images/typing_indicator.gif"
        fillMode: Image.PreserveAspectFit
        anchors.centerIn: parent
    }
}
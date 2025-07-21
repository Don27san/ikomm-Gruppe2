import QtQuick
import QtQuick.Controls

Rectangle {
    id: avatar
    
    property string userInitials: "U"
    property string avatarColor: "#afdeff"
    
    width: 34
    height: 34
    color: avatarColor
    radius: 500

    Image {
        id: ownProfilePicture
        anchors.fill: parent
        source: "../images/grouppicture.png"
        fillMode: Image.PreserveAspectFit
        visible: isOwnMessage
    }
    
    Text {
        text: userInitials
        color: "#9c000000"
        font.pixelSize: 13
        font.styleName: "Bold"
        anchors.centerIn: parent
        visible: !isOwnMessage
    }
}
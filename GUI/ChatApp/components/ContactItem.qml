import QtQuick
import QtQuick.Controls

ItemDelegate {
    id: contactItem
    
    // Properties
    property string contactId: ""
    property string userId: ""
    property string serverName: ""
    property string userInitials: ""
    property string avatarColor: "#afdeff"
    
    // Signals
    signal contactClicked(string contactId)
    
    width: ListView.view ? ListView.view.width : 250
    height: 52
    
    // Background changes based on selection and hover
    background: Rectangle {
        color: contactItem.ListView.isCurrentItem ? "#e3f2fd" : (contactItem.hovered ? "#f5f5f5" : "transparent")
        radius: 4
    }
    
    onClicked: {
        contactItem.ListView.view.currentIndex = index
    }
    
    Row {
        anchors.fill: parent
        anchors.rightMargin: 2
        spacing: 0
        padding: 10
        
        Rectangle {
            id: userIcon
            width: 34
            height: 34
            color: avatarColor
            radius: 17
            anchors.verticalCenter: parent.verticalCenter
            
            Text {
                id: userNameAbbreviated
                color: "#9c000000"
                text: userInitials
                font.pixelSize: 13
                font.styleName: "Bold"
                anchors.centerIn: parent
            }
        }
    }

    Text {
        text: contactId
        anchors.verticalCenter: parent.verticalCenter
        anchors.left: parent.left
        anchors.leftMargin: 50
        font.pixelSize: 15
        font.styleName: contactItem.ListView.isCurrentItem ? "Bold" : "Semibold"
        color: contactItem.ListView.isCurrentItem ? "#1f5cf1" : "#000000"
    }
}
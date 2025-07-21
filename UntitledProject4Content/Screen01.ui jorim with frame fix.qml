

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import UntitledProject4
import QtQuick.Studio.DesignEffects
import QtQuick.Timeline 1.0
import "components"

Rectangle {
    id: rectangle
    width: 750
    height: 700
    color: "#ffffff"

    Row {
        id: row2
        x: 150
        y: 150
        width: 123
        height: 50
        visible: row2.is_visible
        property bool is_visible: false
        padding: 8
        topPadding: 8
        spacing: 10

        Image {
            id: german
            width: 24
            height: 24
            anchors.verticalCenter: parent.verticalCenter
            source: "images/german.png"
            fillMode: Image.PreserveAspectFit
        }

        Text {
            id: text2
            text: qsTr("German")
            anchors.verticalCenter: parent.verticalCenter
            font.pixelSize: 16
            font.styleName: "Medium"
        }

        Connections {
            target: row2
            function onActiveFocusChanged() {
                console.log("clicked")
            }
        }
    }

    Row {
        id: application_container
        anchors.fill: parent

        Rectangle {
            id: contact_section
            width: 250
            color: "#ffffff"
            border.color: "#d0d3d7"
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.leftMargin: -1
            anchors.topMargin: -1
            anchors.bottomMargin: -1

            Frame {
                id: frame1
                height: 66
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.leftMargin: 0
                anchors.rightMargin: 0
                anchors.topMargin: 0
                contentWidth: 690
                    background: Rectangle {
        color: "transparent"
        border.width: 0
    }

                Text {
                    id: text3
                    y: 11
                    text: qsTr("My Contacts")
                    anchors.left: parent.left
                    anchors.leftMargin: 0
                    font.pixelSize: 16
                    font.styleName: "Semibold"
                }

                Button {
                    id: add_contact_button
                    width: 55
                    height: 52
                    text: qsTr("")
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    property bool isActive: false
                    y: 312
                    flat: true
                    Rectangle {
                        id: rectangle5
                        color: "#00ffffff"
                        anchors.fill: parent
                    }

                    Image {
                        id: new_contact
                        width: 20
                        source: "images/new_contact.png"
                        anchors.centerIn: parent
                        fillMode: Image.PreserveAspectFit
                    }

                    Connections {
                        target: add_contact_button
                        function onClicked() {
                            console.log("open new window to add new contact (RecipientUserId & RecipientServerId)")
                        }
                    }
                }
            }

            Column {
                id: contact_container
                anchors.fill: parent
                anchors.topMargin: 66

                Button {
                    id: contact
                    height: 52
                    text: qsTr("")
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.leftMargin: 0
                    anchors.rightMargin: 0
                    flat: true
                    Row {
                        id: row6
                        anchors.fill: parent
                        anchors.rightMargin: 2
                        spacing: 0
                        padding: 10
                        Rectangle {
                            id: user_icon
                            width: 34
                            height: 34
                            color: "#afdeff"
                            radius: 500
                            Text {
                                id: user_name_abbreviated
                                color: "#9c000000"
                                text: qsTr("U1")
                                font.pixelSize: 13
                                font.styleName: "Bold"
                                anchors.centerIn: parent
                            }
                        }
                    }

                    Text {
                        id: text4
                        text: qsTr("<UserId>@<ServerId>")
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: parent.left
                        anchors.leftMargin: 50
                        font.pixelSize: 15
                        font.styleName: "Semibold"
                    }

                    Connections {
                        target: contact
                        function onClicked() {
                            console.log("Open Chat with User <UserId>")
                        }
                    }
                }

                Button {
                    id: contact1
                    height: 52
                    text: qsTr("")
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.leftMargin: 0
                    anchors.rightMargin: 0
                    flat: true
                    Row {
                        id: row7
                        anchors.fill: parent
                        anchors.rightMargin: 2
                        spacing: 0
                        padding: 10
                        Rectangle {
                            id: user_icon1
                            width: 34
                            height: 34
                            color: "#ffafaf"
                            radius: 500
                            anchors.verticalCenter: parent.verticalCenter
                            Text {
                                id: user_name_abbreviated1
                                color: "#9c000000"
                                text: qsTr("U2")
                                font.pixelSize: 13
                                font.styleName: "Bold"
                                anchors.centerIn: parent
                            }
                        }
                    }

                    Text {
                        id: text5
                        text: qsTr("<UserId>@<ServerId>")
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: parent.left
                        anchors.leftMargin: 50
                        font.pixelSize: 15
                        font.styleName: "Semibold"
                    }
                }

                Button {
                    id: contact2
                    height: 52
                    text: qsTr("")
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.leftMargin: 0
                    anchors.rightMargin: 0
                    flat: true
                    Row {
                        id: row8
                        anchors.fill: parent
                        anchors.rightMargin: 2
                        spacing: 0
                        padding: 10
                        Rectangle {
                            id: user_icon2
                            width: 34
                            height: 34
                            color: "#afffc3"
                            radius: 500
                            Text {
                                id: user_name_abbreviated2
                                color: "#9c000000"
                                text: qsTr("U3")
                                font.pixelSize: 13
                                font.styleName: "Bold"
                                anchors.centerIn: parent
                            }
                        }
                    }

                    Text {
                        id: text6
                        text: qsTr("<UserId>@<ServerId>")
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.left: parent.left
                        anchors.leftMargin: 50
                        font.pixelSize: 15
                        font.styleName: "Semibold"
                    }
                }
            }
        }

        Rectangle {
            id: chat_section
            width: 500
            color: "#ffffff"
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.rightMargin: 0
            anchors.topMargin: 0
            anchors.bottomMargin: 0

            Frame {
                id: chat_nav_bar
                height: 66
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.leftMargin: 0
                anchors.rightMargin: 0
                anchors.topMargin: 0
                    background: Rectangle {
        color: "transparent"
        border.width: 0
    }

                Image {
                    id: group
                    width: 37
                    height: 37
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.left: parent.left
                    anchors.leftMargin: 0
                    source: "images/group.png"
                    fillMode: Image.PreserveAspectFit
                }

                Text {
                    id: text1
                    x: 51
                    y: 11
                    text: qsTr("Chat with <UserId>")
                    font.pixelSize: 16
                    font.styleName: "Semibold"
                }

                Image {
                    id: tum
                    x: 427
                    width: 49
                    height: 23
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    source: "images/tum.png"
                    fillMode: Image.PreserveAspectFit
                }
            }

            ScrollView {
                id: scrollView
                anchors.fill: parent
                anchors.topMargin: 66
                anchors.bottomMargin: chat_controls.height
                rightPadding: 10
                leftPadding: 10

                Column {
                    id: chat_container
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.leftMargin: 0
                    anchors.rightMargin: 0
                    spacing: 32

                    Row {
                        id: chat_wrapper_external
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.leftMargin: 0
                        anchors.rightMargin: 0
                        spacing: 4

                        Rectangle {
                            id: user_icon3
                            width: 34
                            height: 34
                            color: "#ffafaf"
                            radius: 500
                            anchors.bottom: parent.bottom
                            anchors.bottomMargin: 0
                            Text {
                                id: user_name_abbreviated3
                                color: "#9c000000"
                                text: qsTr("U2")
                                font.pixelSize: 13
                                font.styleName: "Bold"
                                anchors.centerIn: parent
                            }
                        }

                        Column {
                            id: messages_container
                            width: 400
                            spacing: 6

                            Rectangle {
                                id: live_location_external
                                width: 250
                                height: 105
                                color: "#eeeeee"
                                radius: 16

                                Column {
                                    id: column
                                    anchors.fill: parent
                                    spacing: 8
                                    padding: 12

                                    Row {
                                        id: row
                                        spacing: 8

                                        Rectangle {
                                            id: location_icon
                                            width: 40
                                            height: 40
                                            color: "#1f5cf1"
                                            radius: 500
                                            border.width: 0

                                            Image {
                                                id: location_icon_png
                                                width: 15
                                                source: "images/location_icon.png"
                                                anchors.centerIn: parent
                                                fillMode: Image.PreserveAspectFit
                                            }
                                        }

                                        Column {
                                            id: column1
                                            width: 130
                                            anchors.top: parent.top
                                            anchors.bottom: parent.bottom
                                            anchors.topMargin: 0
                                            anchors.bottomMargin: 0
                                            spacing: 4

                                            Text {
                                                id: text9
                                                text: qsTr("Live Location")
                                                font.pixelSize: 14
                                                font.weight: Font.DemiBold
                                            }

                                            Text {
                                                id: text7
                                                width: 175
                                                color: "#575757"
                                                text: qsTr("<UserID> started sharing")
                                                font.pixelSize: 12
                                                wrapMode: Text.WrapAnywhere
                                            }
                                        }
                                    }

                                    Button {
                                        id: open_location_button
                                        height: 35
                                        text: qsTr("")
                                        anchors.left: parent.left
                                        anchors.right: parent.right
                                        anchors.leftMargin: 12
                                        anchors.rightMargin: 12
                                        property bool isActive: false
                                        flat: true
                                        Rectangle {
                                            id: rectangle6
                                            color: "#fafafa"
                                            radius: 10
                                            anchors.fill: parent
                                        }

                                        Text {
                                            id: text8
                                            text: qsTr("View Location ")
                                            font.pixelSize: 12
                                            font.styleName: "Semibold"
                                            anchors.centerIn: parent
                                        }

                                        Connections {
                                            target: open_location_button
                                            function onClicked() {
                                                console.log("Open link with live location")
                                            }
                                        }
                                    }
                                }
                            }

                            Rectangle {
                                id: message_external
                                color: "#eeeeee"
                                radius: 16
                                width: Math.min(
                                           message_text1.implicitWidth + 24,
                                           400) // max width + padding
                                // Use childrenRect.height + padding for height to capture all content accurately
                                height: message_text1.paintedHeight
                                        + 24 // paintedHeight is more reliable for Text height

                                Text {
                                    id: message_text1
                                    anchors.fill: parent
                                    anchors.margins: 12
                                    text: "wushf ajksd hfjlas fjkadfv "
                                    font.pixelSize: 14
                                    wrapMode: Text.WordWrap
                                    width: parent.width - 24
                                }
                            }

                            Rectangle {
                                id: document_external
                                width: 250
                                height: 105
                                color: "#eeeeee"
                                radius: 16
                                transformOrigin: Item.Center
                                Column {
                                    id: column4
                                    anchors.fill: parent
                                    spacing: 8
                                    padding: 12
                                    Row {
                                        id: row4
                                        spacing: 8
                                        Rectangle {
                                            id: location_icon3
                                            width: 40
                                            height: 40
                                            color: "#1f5cf1"
                                            radius: 500
                                            border.width: 0

                                            Image {
                                                id: document_icon
                                                width: 15
                                                source: "images/document_icon.png"
                                                anchors.centerIn: parent
                                                fillMode: Image.PreserveAspectFit
                                            }
                                        }

                                        Column {
                                            id: column5
                                            width: 130
                                            anchors.top: parent.top
                                            anchors.bottom: parent.bottom
                                            anchors.topMargin: 0
                                            anchors.bottomMargin: 0
                                            spacing: 4
                                            Text {
                                                id: text13
                                                width: 180
                                                text: qsTr("<Name of the file>")
                                                elide: Text.ElideRight
                                                font.pixelSize: 14
                                                font.weight: Font.DemiBold
                                            }

                                            Text {
                                                id: text14
                                                width: 175
                                                color: "#575757"
                                                text: qsTr("<File Size>")
                                                font.pixelSize: 12
                                                wrapMode: Text.WrapAnywhere
                                            }
                                        }
                                    }

                                    Button {
                                        id: open_document_button
                                        height: 35
                                        text: qsTr("")
                                        anchors.left: parent.left
                                        anchors.right: parent.right
                                        anchors.leftMargin: 12
                                        anchors.rightMargin: 12
                                        property bool isActive: false
                                        flat: true
                                        Rectangle {
                                            id: rectangle9
                                            color: "#fafafa"
                                            radius: 10
                                            anchors.fill: parent
                                        }

                                        Text {
                                            id: text15
                                            text: qsTr("Download Document")
                                            font.pixelSize: 12
                                            font.styleName: "Semibold"
                                            anchors.centerIn: parent
                                        }
                                    }
                                }
                            }
                        }
                    }

                    Row {
                        id: chat_wrapper_internal
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.leftMargin: 0
                        anchors.rightMargin: 0
                        layoutDirection: Qt.RightToLeft
                        spacing: 4
                        Rectangle {
                            id: user_icon4
                            width: 34
                            height: 34
                            color: "#afdeff"
                            radius: 500
                            anchors.bottom: parent.bottom
                            anchors.bottomMargin: 0
                            Text {
                                id: user_name_abbreviated4
                                color: "#9c000000"
                                text: qsTr("U1")
                                font.pixelSize: 13
                                font.styleName: "Bold"
                                anchors.centerIn: parent
                            }
                        }

                        Column {
                            id: messages_container1
                            width: 400
                            spacing: 6
                            Rectangle {
                                id: live_location_internal
                                anchors.right: parent.right
                                width: 250
                                height: 105
                                color: "#eeeeee"
                                radius: 16
                                transformOrigin: Item.Center
                                Column {
                                    id: column2
                                    anchors.fill: parent
                                    spacing: 8
                                    padding: 12
                                    Row {
                                        id: row1
                                        spacing: 8
                                        Rectangle {
                                            id: location_icon2
                                            width: 40
                                            height: 40
                                            color: "#1f5cf1"
                                            radius: 500
                                            border.width: 0
                                            Image {
                                                id: location_icon_png1
                                                width: 15
                                                source: "images/location_icon.png"
                                                fillMode: Image.PreserveAspectFit
                                                anchors.centerIn: parent
                                            }
                                        }

                                        Column {
                                            id: column3
                                            width: 130
                                            anchors.top: parent.top
                                            anchors.bottom: parent.bottom
                                            anchors.topMargin: 0
                                            anchors.bottomMargin: 0
                                            spacing: 4
                                            Text {
                                                id: text10
                                                text: qsTr("Live Location")
                                                font.pixelSize: 14
                                                font.weight: Font.DemiBold
                                            }

                                            Text {
                                                id: text11
                                                width: 175
                                                color: "#575757"
                                                text: qsTr("<UserID> started sharing")
                                                font.pixelSize: 12
                                                wrapMode: Text.WrapAnywhere
                                            }
                                        }
                                    }

                                    Button {
                                        id: open_location_button1
                                        height: 35
                                        text: qsTr("")
                                        anchors.left: parent.left
                                        anchors.right: parent.right
                                        anchors.leftMargin: 12
                                        anchors.rightMargin: 12
                                        property bool isActive: false
                                        flat: true
                                        Rectangle {
                                            id: rectangle8
                                            color: "#fafafa"
                                            radius: 10
                                            anchors.fill: parent
                                        }

                                        Text {
                                            id: text12
                                            text: qsTr("View Location ")
                                            font.pixelSize: 12
                                            font.styleName: "Semibold"
                                            anchors.centerIn: parent
                                        }

                                        Connections {
                                            target: open_location_button1
                                            function onClicked() {
                                                console.log("Open link with live location")
                                            }
                                        }
                                    }
                                }
                            }

                            Rectangle {
                                id: message_internal
                                color: "#1f5cf1"
                                radius: 16
                                anchors.right: parent.right
                                anchors.rightMargin: 0
                                width: Math.min(
                                           message_text_internal.implicitWidth + 24,
                                           400) // max width + padding
                                height: message_text_internal.paintedHeight
                                        + 24 // actual text height + padding

                                Text {
                                    id: message_text_internal
                                    anchors.fill: parent
                                    anchors.margins: 12
                                    text: "Longer messages will take up more width than smaller messages that dont need it."
                                    font.pixelSize: 14
                                    color: "#ffffff"
                                    wrapMode: Text.WordWrap
                                    horizontalAlignment: Text.AlignLeft
                                    // width dynamically fills container minus padding
                                    width: parent.width - 24
                                }
                            }

                            Rectangle {
                                id: message_internal1
                                width: Math.min(
                                           message_text_internal1.implicitWidth + 24,
                                           400)
                                height: message_text_internal1.paintedHeight + 24
                                color: "#1f5cf1"
                                radius: 16
                                anchors.right: parent.right
                                anchors.rightMargin: 0
                                Text {
                                    id: message_text_internal1
                                    width: parent.width - 24
                                    color: "#ffffff"
                                    text: "fdfsdfasdf"
                                    anchors.fill: parent
                                    anchors.margins: 12
                                    font.pixelSize: 14
                                    horizontalAlignment: Text.AlignLeft
                                    wrapMode: Text.WordWrap
                                }
                            }
                        }
                    }

                    Row {
                        id: chat_wrapper_external1
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.leftMargin: 0
                        anchors.rightMargin: 0
                        spacing: 4
                        Rectangle {
                            id: user_icon5
                            width: 34
                            height: 34
                            color: "#ffafaf"
                            radius: 500
                            anchors.bottom: parent.bottom
                            anchors.bottomMargin: 0
                            Text {
                                id: user_name_abbreviated5
                                color: "#9c000000"
                                text: qsTr("U2")
                                font.pixelSize: 13
                                font.styleName: "Bold"
                                anchors.centerIn: parent
                            }
                        }

                        Column {
                            id: messages_container2
                            width: 400
                            spacing: 6

                            Rectangle {
                                id: typing_indicator1
                                width: 60
                                height: 36
                                color: "#eeeeee"
                                radius: 16
                                AnimatedImage {
                                    id: typing_indicator_animation1
                                    width: 50
                                    source: "images/typing_indicator.gif"
                                    fillMode: Image.PreserveAspectFit
                                    anchors.centerIn: parent
                                }
                            }
                        }
                    }
                }
            }

            Rectangle {
                id: chat_controls
                height: row3.implicitHeight
                color: "#ffffff"
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.leftMargin: 0
                anchors.rightMargin: 0
                anchors.bottomMargin: 0

                Row {
                    id: row3
                    anchors.fill: parent
                    spacing: 4
                    padding: 10

                    ComboBox {
                        id: comboBox
                        width: 50
                        height: input_comp.height
                        clip: true
                        textRole: "text"
                        indicator: Item {}

                        model: ListModel {
                            ListElement {
                                text: ""
                            } // ⬅️ Default item, triggers icon
                            ListElement {
                                text: "🇩🇪"
                            }
                            ListElement {
                                text: "🇨🇳"
                            }
                            ListElement {
                                text: "🇬🇧"
                            }
                            ListElement {
                                text: "🇹🇷"
                            }
                        }

                        onActivated: comboBox.focus = false

                        background: Rectangle {
                            color: "white"
                            radius: 6
                            border.width: 2
                            border.color: (comboBox.focus
                                           || comboBox.popup.visible) ? "#1f5cf1" : "transparent"
                        }

                        popup: Popup {
                            y: comboBox.height
                            width: comboBox.width
                            implicitHeight: contentItem.implicitHeight
                            padding: 0
                            background: Rectangle {
                                color: "white"
                                border.color: "#cccccc" // subtle gray border
                                border.width: 1
                                radius: 6
                            }

                            contentItem: ListView {
                                clip: true
                                implicitHeight: contentHeight
                                model: comboBox.delegateModel
                                currentIndex: comboBox.highlightedIndex
                                interactive: true
                                delegate: comboBox.delegate
                            }
                        }

                        // Show the flag only if a real selection is made
                        contentItem: Text {
                            anchors.centerIn: parent
                            text: comboBox.currentIndex > 0 ? comboBox.currentText : ""
                            font.pixelSize: 20
                            horizontalAlignment: Text.AlignHCenter
                            verticalAlignment: Text.AlignVCenter
                        }

                        // Show the translation icon when no country is selected (default state)
                        Image {
                            id: translation
                            width: 32
                            height: 23
                            source: "images/translation.png"
                            anchors.centerIn: parent
                            fillMode: Image.PreserveAspectFit
                            visible: comboBox.currentIndex === 0
                        }

                        // Optional: Clean look for popup items
                        delegate: ItemDelegate {
                            width: comboBox.width
                            contentItem: Text {
                                text: model.text === "" ? "-" : model.text
                                font.pixelSize: 20
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                        }

                        // Set default index to 0
                        Component.onCompleted: comboBox.currentIndex = 0
                    }

                    Button {
                        id: location
                        height: input_comp.height
                        text: qsTr("")
                        property bool isActive: false
                        width: 40
                        flat: true
                        Rectangle {
                            id: rectangle7
                            color: "#ffffff"
                        }

                        Image {
                            id: location_icon1
                            x: -201
                            y: 62
                            width: 30
                            height: 28
                            source: "images/marker.png"
                            fillMode: Image.PreserveAspectFit
                            anchors.centerIn: parent
                        }
                    }
                    Rectangle {
                        id: input_comp
                        width: 380
                        height: textEdit.implicitHeight
                        color: "#eeeeee"
                        radius: 15

                        TextEdit {
                            id: textEdit
                            height: textEdit.implicitHeight
                            text: qsTr("Send a message")
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.leftMargin: 0
                            anchors.rightMargin: 0
                            font.pixelSize: 14
                            verticalAlignment: Text.AlignVCenter
                            wrapMode: Text.Wrap
                            font.styleName: "Medium"
                            rightPadding: 50
                            leftPadding: 12
                            bottomPadding: 12
                            topPadding: 12
                            clip: false
                        }

                        Button {
                            id: send_button
                            x: 166
                            width: 34
                            text: qsTr("")
                            anchors.right: parent.right
                            anchors.top: parent.top
                            anchors.bottom: parent.bottom
                            anchors.rightMargin: 9
                            anchors.topMargin: 0
                            anchors.bottomMargin: 0
                            icon.color: "#00ffffff"
                            flat: true
                            Rectangle {
                                id: rectangle3
                                color: "#00ffffff"
                                anchors.fill: parent
                                anchors.topMargin: 0
                            }

                            Image {
                                id: send
                                width: 31
                                height: 20
                                source: "images/send.png"
                                anchors.centerIn: parent
                                fillMode: Image.PreserveAspectFit
                            }
                        }
                    }
                }
            }
        }
    }
}

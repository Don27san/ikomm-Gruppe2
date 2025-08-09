import QtQuick
import "components"

Window {
    width: mainScreen.width
    height: mainScreen.height

    visible: true
    title: "ChatApp"

    Screen01 {
        id: mainScreen
    }

    onClosing: {
        // Handle Cleanup
        chatBackend.closeEvent()
    }

}

